import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import platform  # 👈 Importar para detectar el sistema operativo

# Solo importar si estás en Windows
if platform.system() == "Windows":
    import pythoncom
    import win32com.client

def base_de_datos():
    if st.button("Regresar"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

    # Encabezado
    col1, col2 = st.columns([1, 5])
    with col1:
        st.title("Gestión de la Base de Datos")
    with col2:
        st.image("GREENBRIERLOGO.png", width=100)
    
    st.text("Aquí irá la base de datos de todos los ítems")
