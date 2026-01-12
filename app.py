# =========================
# IMPORTACIONES
# =========================
import os
import time
import json

import gspread
from google.oauth2.service_account import Credentials

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory
)

from datetime import datetime, timedelta


# =========================
# ZONA HORARIA
# =========================
os.environ["TZ"] = "America/Mexico_City"

# tzset solo existe en Linux / macOS
if hasattr(time, "tzset"):
    time.tzset()


# =========================
# CONFIGURACIÓN FLASK
# =========================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "keytronics123")
app.permanent_session_lifetime = timedelta(minutes=30)


# =========================
# GOOGLE SHEETS
# =========================
GOOGLE_SHEETS_ID = os.environ.get(
    "GOOGLE_SHEETS_ID",
    "14x3JapIuLdgclmk4_ls3NCMWZVJF5fjNhyIGI6G86dE"
)

CREDENCIALES_JSON = "credenciales_google.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

print("🔍 Intentando cargar credenciales (ENV o archivo)...")

sheet = None

try:
    google_credentials_env = os.environ.get("GOOGLE_CREDENTIALS")

    if google_credentials_env:
        # Render / Producción
        creds_info = json.loads(google_credentials_env)
        credentials = Credentials.from_service_account_info(
            creds_info,
            scopes=SCOPES
        )
        print("🔑 Credenciales cargadas desde variable de entorno.")
    else:
        # Desarrollo local
        credentials = Credentials.from_service_account_file(
            CREDENCIALES_JSON,
            scopes=SCOPES
        )
        print("🔑 Credenciales cargadas desde archivo local.")

    client = gspread.authorize(credentials)
    sheet = client.open_by_key(GOOGLE_SHEETS_ID).sheet1

    print("✅ Conexión exitosa con Google Sheets.")

except Exception as e:
    print("⚠️ Error conectando con Google Sheets:", e)
    sheet = None


# =========================
# USUARIOS PERMITIDOS
# =========================
USUARIOS = {
    "Jose_Consultor": {
        "password": "654321987",
        "roles": ["reporte_1", "reporte_2"]
    },

    "AlfonsoCampo": {
        "password":"N7$vL8qY#x3B",
        "roles": ["reporte_1", "reporte_2"]
    },

    "AlejandroCampo": {
        "password": "tR!5mK2wQ9#z",
        "roles": ["reporte_1"]
    },

    "DavidVargas": {
        "password":"Fp8#Vd4!sZ1q",
        "roles": ["reporte_1"]
    },

    "BrendaMuñoz": {
        "password":"H2!xW7qR#k9L",
        "roles": ["reporte_1"]
    },

    "VidalCamacho": {
        "password": "b9#Zt6Pq!M3r",
        "roles": ["reporte_1"]
    },

    "HumbertoColin": {
        "password":"Gv3!Qw8#xN5z",
        "roles": ["reporte_1"]
    },

    "JaimeFontanet": {
        "password":"L1#pT9v!R6kS",
        "roles": ["reporte_1", "reporte_2"]
    },

    "AlbertoEchavarria": {
        "password":"s4!Kz7Q#n2Wm",
        "roles": ["reporte_1"]
    },

    "Laura": {
        "password":"Y8!fR5p#T1qZ",
        "roles": ["reporte_2"]
    }
}

POWER_BI_REPORTES = {
    "reporte_1": "https://app.powerbi.com/view?r=eyJrIjoiMWQzYzgyNmEtODdmYS00YWNmLWJhMmQtNmIyMmYzNWY4ODY1IiwidCI6IjAzODk5MTIxLWQ5NzYtNDRlOS1iODI0LTFmYzU1N2JmZGRjZSJ9",
    "reporte_2": "https://app.powerbi.com/view?r=eyJrIjoiOTdjYmNlZjEtYWQ0Yy00YjUyLWE5Y2MtYWMwZmYwM2E3ZGU5IiwidCI6IjAzODk5MTIxLWQ5NzYtNDRlOS1iODI0LTFmYzU1N2JmZGRjZSJ9"
}

# =========================
# FUNCIÓN: REGISTRAR ACCESO
# =========================
def registrar_acceso(usuario):
    print("🚨 registrar_acceso() llamado por:", usuario)

    if not sheet:
        print("⚠️ No hay conexión con Google Sheets.")
        return

    try:
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")

        sheet.append_row([usuario, fecha, hora])
        print(f"✅ Acceso registrado: {usuario} - {fecha} {hora}")

    except Exception as e:
        print("❌ Error al guardar en Google Sheets:", e)


# =========================
# RUTAS
# =========================
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    u = request.form["username"]
    p = request.form["password"]

    if u in USUARIOS and USUARIOS[u]["password"] == p:
        session["user"] = u
        session["roles"] = USUARIOS[u]["roles"]
        registrar_acceso(u)
        return redirect("/dashboard")

    return render_template("login.html", error="Credenciales incorrectas")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("selector_reportes.html", roles=session["roles"])

@app.route("/reporte/<reporte_id>")
def ver_reporte(reporte_id):
    if "user" not in session:
        return redirect(url_for("home"))

    if reporte_id not in POWER_BI_REPORTES:
        return "Reporte no existe", 404

    if reporte_id not in session.get("roles", []):
        return "⛔ Sin permiso", 403

    return render_template(
        "dashboard.html",
        embed_url=POWER_BI_REPORTES[reporte_id],
        mostrar_descarga=reporte_id == "reporte_1"
    )

@app.route("/descargar_csv")
def descargar_csv():
    if "user" not in session:
        return redirect(url_for("home"))

    return send_from_directory(
        os.getcwd(),
        "datos_reporte_Keytronics.xlsx",
        as_attachment=True
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("🚀 Servidor iniciando en puerto:", port)
    app.run(host="0.0.0.0", port=port, debug=False)
