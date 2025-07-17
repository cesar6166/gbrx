import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import win32com.client
import pythoncom

def base_de_datos():
    if st.button("Regresar"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

    st.title("Gestión de la Base de Datos")
    st.text("Aqui ira la base de datos de todos los items")

    