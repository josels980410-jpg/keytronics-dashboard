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
        "roles": ["reporte_1", "reporte_2"]
    },

    "HumbertoColin": {
        "password":"Gv3!Qw8#xN5z",
        "roles": ["reporte_1", "reporte_2"]
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
    username = request.form["username"]
    password = request.form["password"]

    print("\n==========================")
    print("➡️ Intentando login con:", username)
    print("==========================")

    if username in USUARIOS and USUARIOS[username] == password:
        print("✔ Login exitoso")

        session.permanent = True
        session["user"] = username
        session["roles"] = USUARIOS[username]["roles"]

        registrar_acceso(username)
        return redirect(url_for("dashboard"))

    print("❌ Login fallido")
    return render_template(
        "login.html",
        error="Usuario o contraseña incorrectos"
    )


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    embed_url = (
        "https://app.powerbi.com/view?r=eyJrIjoiMWQzYzgyNmEtODdmYS00YWNmLWJhMmQtNmIyMmYzNWY4ODY1IiwidCI6IjAzODk5MTIxLWQ5NzYtNDRlOS1iODI0LTFmYzU1N2JmZGRjZSJ9"
    )

    return f"""
    <html>
    <head>
        <title>Dashboard Power BI</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #0a0a0a;
                color: #00ff80;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
                margin: 0;
            }}
            h2 {{
                text-shadow: 0 0 8px #00ff80;
            }}
            iframe {{
                width: 95%;
                height: 85vh;
                border-radius: 10px;
                box-shadow: 0 0 25px #00ff80;
            }}
            .top-buttons {{
                position: absolute;
                top: 15px;
                right: 25px;
                display: flex;
                gap: 10px;
            }}
            .btn {{
                border: 1px solid #00ff80;
                color: #00ff80;
                padding: 8px 15px;
                border-radius: 6px;
                text-decoration: none;
            }}
            .btn:hover {{
                background: #00ff80;
                color: #0a0a0a;
            }}
        </style>
    </head>
    <body>
        <div class="top-buttons">
            <a href="{url_for('descargar_csv')}" class="btn">📄 Reporte</a>
            <a href="{url_for('logout')}" class="btn">Cerrar sesión</a>
        </div>

        <h2>Bienvenido</h2>
        <iframe src="{embed_url}" allowfullscreen></iframe>
    </body>
    </html>
    """


@app.route("/descargar_csv")
def descargar_csv():
    if "user" not in session:
        return redirect(url_for("home"))

    directorio = os.path.dirname(os.path.abspath(__file__))
    archivo = "datos_reporte_Keytronics.xlsx"

    return send_from_directory(
        directory=directorio,
        path=archivo,
        as_attachment=True
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("🚀 Servidor iniciando en puerto:", port)
    app.run(host="0.0.0.0", port=port, debug=False)
