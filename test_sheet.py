import gspread
from google.oauth2.service_account import Credentials

CREDENCIALES_JSON = "credenciales_google.json"
GOOGLE_SHEETS_ID = "1qExzOzO2YIK_ldAZsHFcQtHbBVHxIhQNKrg3kT6S1rI"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = Credentials.from_service_account_file(CREDENCIALES_JSON, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open_by_key(GOOGLE_SHEETS_ID).sheet1

# Prueba de escritura
sheet.append_row(["TEST", "Prueba Service Account"])
print("✅ Fila agregada correctamente")
