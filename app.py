import streamlit as st
import pandas as pd

st.set_page_config(page_title="Directorio de Apps", layout="wide")
st.title("Directorio de Aplicaciones")

# --- Configuración del administrador ---
ADMIN_USUARIO = "admin"
ADMIN_CLAVE = "1234"  # Puedes cambiar esta clave por una más segura

# --- Inicializar almacenamiento en memoria ---
if "apps" not in st.session_state:
    st.session_state.apps = pd.DataFrame(columns=["Nombre", "Descripción", "Enlace"])

# --- Inicializar campos del formulario ---
for campo in ["nombre_input", "descripcion_input", "enlace_input"]:
    if campo not in st.session_state:
        st.session_state[campo] = ""

def limpiar_formulario():
    st.session_state["nombre_input"] = ""
    st.session_state["descripcion_input"] = ""
    st.session_state["enlace_input"] = ""

# --- Sidebar: Login de administrador ---
with st.sidebar:
    st.markdown("### Acceso de administrador")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
    es_admin = usuario == ADMIN_USUARIO and clave == ADMIN_CLAVE

# --- Si es administrador: mostrar formulario de carga ---
if es_admin:
    st.success("Modo administrador activado. Puedes agregar nuevas aplicaciones.")
    
    with st.form("add_app_form"):
        nombre = st.text_input("Nombre de la Aplicación", value=st.session_state["nombre_input"], key="nombre_input")
        descripcion = st.text_area("Descripción", value=st.session_state["descripcion_input"], key="descripcion_input")
        enlace = st.text_input("Enlace (URL)", value=st.session_state["enlace_input"], key="enlace_input")
        submit = st.form_submit_button("Agregar Aplicación")

        if submit and nombre and enlace:
            nueva_app = pd.DataFrame([[nombre, descripcion, enlace]], columns=["Nombre", "Descripción", "Enlace"])
            st.session_state.apps = pd.concat([st.session_state.apps, nueva_app], ignore_index=True)
            st.success("Aplicación agregada exitosamente")
            limpiar_formulario()
else:
    st.info("Solo lectura. Para agregar aplicaciones, ingresa como administrador en el menú lateral.")

# --- Mostrar listado de aplicaciones ---
def hacer_clickable(val):
    return f'<a href="{val}" target="_blank">Abrir</a>' if val else ""

st.markdown("## Aplicaciones Registradas")
if not st.session_state.apps.empty:
    tabla = st.session_state.apps.copy()
    tabla["Enlace"] = tabla["Enlace"].apply(hacer_clickable)
    st.write(tabla.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.warning("No hay aplicaciones registradas todavía.")
