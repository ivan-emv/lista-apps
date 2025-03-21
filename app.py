import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# --- Configuración de acceso ---
SHEET_NAME = "Directorio Apps"
WORKSHEET_NAME = "Apps"

# --- Conexión a Google Sheets ---
@st.cache_resource
def conectar_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)
    return sheet

# --- Cargar datos desde la hoja ---
def cargar_datos(sheet):
    df = get_as_dataframe(sheet, evaluate_formulas=True, dtype=str).dropna(how="all")
    return df if not df.empty else pd.DataFrame(columns=["Nombre", "Descripción", "Enlace"])

# --- Guardar datos ---
def guardar_datos(sheet, df):
    sheet.clear()
    set_with_dataframe(sheet, df)

# --- Configuración app ---
st.set_page_config(page_title="Directorio de Apps", layout="wide")
st.title("Directorio de Aplicaciones")

ADMIN_USUARIO = "admin"
ADMIN_CLAVE = "1234"

sheet = conectar_gsheet()
if "apps" not in st.session_state:
    st.session_state.apps = cargar_datos(sheet)
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# --- Sidebar autenticación ---
with st.sidebar:
    st.markdown("### Acceso de administrador")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
    es_admin = usuario == ADMIN_USUARIO and clave == ADMIN_CLAVE

# --- Formulario para admins ---
if es_admin:
    st.success("Modo administrador activado. Puedes agregar nuevas aplicaciones.")

    if st.session_state.reset_form:
        st.session_state["nombre"] = ""
        st.session_state["descripcion"] = ""
        st.session_state["enlace"] = ""
        st.session_state.reset_form = False

    with st.form("add_app_form"):
        nombre = st.text_input("Nombre de la Aplicación", key="nombre")
        descripcion = st.text_area("Descripción", key="descripcion")
        enlace = st.text_input("Enlace (URL)", key="enlace")
        submit = st.form_submit_button("Agregar Aplicación")

        if submit and nombre and enlace:
            nueva_app = pd.DataFrame([[nombre, descripcion, enlace]], columns=["Nombre", "Descripción", "Enlace"])
            st.session_state.apps = pd.concat([st.session_state.apps, nueva_app], ignore_index=True)
            guardar_datos(sheet, st.session_state.apps)
            st.success("Aplicación agregada exitosamente")
            st.session_state.reset_form = True
            st.experimental_rerun()
else:
    st.info("Solo lectura. Para agregar aplicaciones, ingresa como administrador.")

# --- Mostrar apps ---
def hacer_clickable(val):
    return f'<a href="{val}" target="_blank">Abrir</a>' if val else ""

st.markdown("## Aplicaciones Registradas")
if not st.session_state.apps.empty:
    tabla = st.session_state.apps.copy()
    tabla["Enlace"] = tabla["Enlace"].apply(hacer_clickable)
    st.write(tabla.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.warning("No hay aplicaciones registradas todavía.")
