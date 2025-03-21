import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# Configuración
st.set_page_config(page_title="Directorio de Apps", layout="wide")
st.title("📁 Directorio de Aplicaciones")

# Datos de Google Sheets
SHEET_NAME = "Directorio Apps"
WORKSHEET_NAME = "Apps"

# Conectar con Google Sheets
@st.cache_resource
def conectar_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# Cargar datos desde la hoja
def cargar_datos(sheet):
    df = get_as_dataframe(sheet, evaluate_formulas=True, dtype=str).dropna(how="all")
    return df if not df.empty else pd.DataFrame(columns=["Nombre", "Descripción", "Enlace"])

# Guardar datos en la hoja
def guardar_datos(sheet, df):
    sheet.clear()
    set_with_dataframe(sheet, df)

# Conexión a la hoja
hoja = conectar_gsheet()
if "apps" not in st.session_state:
    st.session_state.apps = cargar_datos(hoja)

# Autenticación simple de administrador
with st.sidebar:
    st.markdown("### 🔐 Acceso de administrador")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
    es_admin = usuario == "ivan.amador" and clave == "EMVac1997-"

# Bandera para evitar rerun directo dentro del formulario
if "app_agregada" not in st.session_state:
    st.session_state.app_agregada = False

# Mostrar formulario solo para admins
if es_admin:
    st.success("Modo administrador activado. Puedes agregar nuevas aplicaciones.")

    if st.session_state.app_agregada:
        st.session_state.app_agregada = False
        st.experimental_rerun()

    with st.form("formulario_agregar"):
        nombre = st.text_input("Nombre de la Aplicación")
        descripcion = st.text_area("Descripción")
        enlace = st.text_input("Enlace (URL)")
        enviar = st.form_submit_button("Agregar Aplicación")

        if enviar and nombre and enlace:
            nueva_fila = pd.DataFrame([[nombre, descripcion, enlace]], columns=["Nombre", "Descripción", "Enlace"])
            st.session_state.apps = pd.concat([st.session_state.apps, nueva_fila], ignore_index=True)
            guardar_datos(hoja, st.session_state.apps)
            st.success("✅ Aplicación agregada exitosamente")
            st.session_state.app_agregada = True
else:
    st.info("🔍 Solo lectura. Inicia sesión como administrador para agregar aplicaciones.")

# Mostrar tabla de aplicaciones
st.markdown("## 📋 Aplicaciones Registradas")
def hacer_clickable(url):
    return f'<a href="{url}" target="_blank">Abrir</a>' if url else ""

if not st.session_state.apps.empty:
    df_display = st.session_state.apps.copy()
    df_display["Enlace"] = df_display["Enlace"].apply(hacer_clickable)
    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.warning("No hay aplicaciones registradas todavía.")
