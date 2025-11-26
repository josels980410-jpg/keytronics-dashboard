import gspread
import json
from google.oauth2 import service_account

print("\n🔍 INICIANDO TEST DE GOOGLE SHEETS\n")

# =======================================================
# Cargar credenciales
# =======================================================
with open("credenciales_google.json") as f:
    creds_json = json.load(f)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = service_account.Credentials.from_service_account_info(creds_json, scopes=SCOPES)

client = gspread.authorize(creds)

# =======================================================
# ABRIR EL SPREADSHEET
# =======================================================
SPREADSHEET_ID = "14x3JapIuLdgclmk4_ls3NCMWZVJF5fjNhyIGI6G86dE"
sh = client.open_by_key(SPREADSHEET_ID)

# Mostrar hojas existentes
hojas = [w.title for w in sh.worksheets()]
print("📄 Hojas encontradas:", hojas)

# =======================================================
# Intentar escribir en la PRIMERA hoja del archivo
# =======================================================
try:
    ws = sh.sheet1
    ws.append_row(["Registro de prueba"])
    print("✅ SE ESCRIBIÓ EN:", ws.title)
except Exception as e:
    print("❌ ERROR AL ESCRIBIR:", e)
