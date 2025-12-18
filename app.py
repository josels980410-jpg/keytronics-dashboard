import os
import time
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from datetime import datetime, timedelta, date


# ------------------- ZONA HORARIA ------------------- 
os.environ['TZ'] = 'America/Mexico_City'

if hasattr(time, "tzset"):
    time.tzset()



# ------------------- CONFIGURACIÓN FLASK -------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "keytronics123")
app.permanent_session_lifetime = timedelta(minutes=30)

# ------------------- GOOGLE SHEETS -------------------
GOOGLE_SHEETS_ID = os.environ.get("GOOGLE_SHEETS_ID", "14x3JapIuLdgclmk4_ls3NCMWZVJF5fjNhyIGI6G86dE")
CREDENCIALES_JSON = "credenciales_google.json"  
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

print("🔍 Intentando cargar credenciales (ENV or file)...")

sheet = None
try:
    google_credentials_env = os.environ.get("GOOGLE_CREDENTIALS")
    if google_credentials_env:
        import json
        creds_info = json.loads(google_credentials_env)
        credentials = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
        print("🔑 Credenciales cargadas desde GOOGLE_CREDENTIALS (env).")
    else:
        credentials = Credentials.from_service_account_file(CREDENCIALES_JSON, scopes=SCOPES)
        print("🔑 Credenciales cargadas desde archivo local.")

    client = gspread.authorize(credentials)
    sheet = client.open_by_key(GOOGLE_SHEETS_ID).sheet1
    print("✅ Conexión exitosa con Google Sheets (Service Account).")
except Exception as e:
    print("⚠️ Error conectando con Google Sheets:", e)
    sheet = None


# ------------------- USUARIOS PERMITIDOS -------------------
USUARIOS = {
    "Jose_Consultor": "654321987",
    "AlfonsoCampo": "N7$vL8qY#x3B",
    "AlejandroCampo": "tR!5mK2wQ9#z",
    "DavidVargas": "Fp8#Vd4!sZ1q",
    "BrendaMuñoz": "H2!xW7qR#k9L",
    "VidalCamacho": "b9#Zt6Pq!M3r",
    "HumbertoColin": "Gv3!Qw8#xN5z",
    "JaimeFontanet": "L1#pT9v!R6kS",
    "AlbertoEchavarria": "s4!Kz7Q#n2Wm",
    "usuario10": "Y8!fR5p#T1qZ"
}


# ------------------- FUNCIÓN: REGISTRAR ACCESO -------------------
def registrar_acceso(usuario):
    print("🚨 registrar_acceso() fue llamado por:", usuario)

    if not sheet:
        print("⚠️ No hay conexión con Google Sheets. No se registró acceso.")
        return

    try:
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")
        print("✏️ Intentando escribir en Google Sheets...")
        sheet.append_row([usuario, fecha, hora])
        print(f"✅ Acceso registrado: {usuario} - {fecha} {hora}")
    except Exception as e:
        print("❌ ERROR al guardar en Google Sheets:", e)


# ------------------- FUNCIÓN: MENSAJE DE VIGENCIA -------------------
def obtener_mensaje_vigencia():
    hoy = date.today()
    fecha_limite = date(2025, 12, 31)

    if hoy <= fecha_limite:
        return (
            "Este sistema se encuentra en fase de demostración y evaluación.<br><br>"
            "La vigencia de esta versión está contemplada hasta el "
            "<strong>31 de diciembre</strong>.<br><br>"
            "Para cualquier duda o continuidad del servicio, favor de contactar al proveedor."
        )
    else:
        return (
            "<strong>La vigencia ha finalizado.</strong><br><br>"
            "Favor de contactar al proveedor para la reactivación del servicio."
        )


# ------------------- RUTA: LOGIN -------------------
@app.route("/")
def home():
    mensaje_vigencia = obtener_mensaje_vigencia()
    return render_template("login.html", mensaje_vigencia=mensaje_vigencia)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    print("\n==========================")
    print("➡️ Intentando login con:", username)
    print("==========================")

    if username in USUARIOS and USUARIOS[username] == password:
        print("✔ Usuario y contraseña correctos")

        session.permanent = True
        session["user"] = username

        registrar_acceso(username)

        return redirect(url_for("dashboard"))
    else:
        print("❌ Login falló")
        mensaje_vigencia = obtener_mensaje_vigencia()
        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos",
            mensaje_vigencia=mensaje_vigencia
        )


# ------------------- RUTA: DASHBOARD -------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    embed_url = "https://app.powerbi.com/view?r=eyJrIjoiYzk3YTJkYmYtYTcwOS00MmE4LWIwMzMtYWRhZGZkM2RiMTkxIiwidCI6IjAzODk5MTIxLWQ5NzYtNDRlOS1iODI0LTFmYzU1N2JmZGRjZSJ9"

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
                    justify-content: flex-start;
                    padding: 20px;
                    height: 100vh;
                    margin: 0;
                }}
                h2 {{
                    margin-bottom: 15px;
                    color: #00ff80;
                    text-shadow: 0 0 8px #00ff80;
                }}
                iframe {{
                    width: 95%;
                    height: 85vh;
                    border: none;
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
                    background-color: transparent;
                    color: #00ff80;
                    border: 1px solid #00ff80;
                    padding: 8px 15px;
                    border-radius: 6px;
                    text-decoration: none;
                    transition: 0.3s;
                }}
                .btn:hover {{
                    background-color: #00ff80;
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

            <iframe src="{embed_url}" allowfullscreen="true"
                sandbox="allow-same-origin allow-scripts allow-forms"></iframe>
        </body>
    </html>
    """


# ------------------- DESCARGA ARCHIVO -------------------
@app.route("/descargar_csv")
def descargar_csv():
    if "user" not in session:
        return redirect(url_for("home"))

    directorio = os.path.dirname(os.path.abspath(__file__))
    archivo = "datos_reporte_Keytronics.xlsx"

    return send_from_directory(directory=directorio, path=archivo, as_attachment=True)


# ------------------- LOGOUT -------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


# ------------------- EJECUCIÓN -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("🚀 Servidor iniciando en puerto:", port)
    app.run(host="0.0.0.0", port=port, debug=False)
