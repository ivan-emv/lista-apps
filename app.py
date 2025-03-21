import streamlit as st
import pandas as pd

st.title("Directorio de Aplicaciones")

if "apps" not in st.session_state:
    st.session_state.apps = pd.DataFrame(columns=["Nombre", "Descripción", "Enlace"])

with st.form("add_app_form"):
    nombre = st.text_input("Nombre de la Aplicación")
    descripcion = st.text_area("Descripción")
    enlace = st.text_input("Enlace (URL)")
    submit = st.form_submit_button("Agregar Aplicación")

    if submit and nombre and enlace:
        nueva_app = pd.DataFrame([[nombre, descripcion, enlace]], columns=["Nombre", "Descripción", "Enlace"])
        st.session_state.apps = pd.concat([st.session_state.apps, nueva_app], ignore_index=True)
        st.success("Aplicación agregada exitosamente")

def hacer_clickable(val):
    return f'<a href="{val}" target="_blank">Abrir</a>' if val else ""

st.markdown("## Aplicaciones Registradas")
if not st.session_state.apps.empty:
    tabla = st.session_state.apps.copy()
    tabla["Enlace"] = tabla["Enlace"].apply(hacer_clickable)
    st.write(tabla.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("No hay aplicaciones registradas todavía.")
