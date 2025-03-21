import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("🔧 Test de conexión a Google Sheets")

# Nombre de la hoja y pestaña que creaste
SHEET_NAME = "Directorio Apps"
WORKSHEET_NAME = "Apps"

# Conexión a Google Sheets
def conectar_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

try:
    hoja = conectar_gsheet()
    st.success("✅ Conexión exitosa a Google Sheets")

    # Mostrar contenido de la hoja (primeros 10 registros)
    datos = hoja.get_all_records()
    st.write("📋 Contenido actual de la hoja:")
    st.dataframe(datos)

    # Agregar una fila de prueba (comentada por si no deseas escribir nada)
    if st.button("➕ Agregar fila de prueba"):
        hoja.append_row(["App de prueba", "Descripción de prueba", "https://prueba.app"])
        st.success("Fila de prueba agregada correctamente")

except Exception as e:
    st.error("❌ Error al conectar con Google Sheets:")
    st.text(f"{type(e).__name__}: {e}")

