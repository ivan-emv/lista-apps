import streamlit as st
import pandas as pd

st.set_page_config(page_title="Directorio de Apps", layout="wide")
st.title("Directorio de Aplicaciones")

# --- Configuración del administrador ---
ADMIN_USUARIO = "ivanedu113"
ADMIN_CLAVE = "EMVac1997-"

# --- Inicializar almacenamiento de aplicaciones ---
if "apps" not in st.session_state:
    st.session_state.apps = pd.DataFrame(columns=["Nombre", "Descripción", "Enlace"])

# --- Inicializar valores de entrada del formulario ---
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# --- Sidebar para autenticación ---
with st.sidebar:
    st.markdown("### Acceso de administrador")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
    es_admin = usuario == ADMIN_USUARIO and clave == ADMIN_CLAVE

# --- Mostrar formulario si es administrador ---
if es_admin:
    st.success("Modo administrador activado. Puedes agregar nuevas aplicaciones.")

    # Si se activó el reset del formulario, se borra el estado
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
            st.success("Aplicación agregada exitosamente")
            st.session_state.reset_form = True
            st.experimental_rerun()  # Vuelve a cargar la app para limpiar los campos
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
