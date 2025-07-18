import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import platform 

# Solo importar si estás en Windows
if platform.system() == "Windows":
    import pythoncom
    import win32com.client

def items():
    if st.button("Regresar"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

    st.title("Catalagos")
