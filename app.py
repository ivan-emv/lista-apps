import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Test de Google Sheets", layout="wide")
st.title("🔧 Test de conexión con Google Sheets")

# Datos de tu hoja de cálculo
SHEET_NAME = "Directorio Apps"
WORKSHEET_NAME = "Apps"

# Función para conectar a Google Sheets
def conectar_gsheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)
    return sheet

# Intentar conexión
try:
    hoja = conectar_gsheet()
    st.success("✅ Conexión exitosa a Google Sheets")

    # Mostrar contenido actual
    datos = hoja.get_all_records()
    st.write("📋 Datos actuales:")
    st.dataframe(datos)

    # Opción para agregar una fila de prueba
    if st.button("➕ Agregar fila de prueba"):
        hoja.append_row(["App de prueba", "Esta es una prueba desde Streamlit", "https://appdeprueba.com"])
        st.success("✅ Fila de prueba agregada correctamente")

except Exception as e:
    st.error("❌ Error al conectar con Google Sheets:")
    st.text(f"{type(e).__name__}: {e}")
