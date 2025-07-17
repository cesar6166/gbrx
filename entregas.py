import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import win32com.client
import pythoncom
import sqlite3

def obtener_usuario_desde_db():
    try:
        conn = sqlite3.connect("Warehouse.db")
        cursor = conn.cursor()

        # Aquí puedes ajustar la consulta según tu estructura
        cursor.execute("SELECT usuario FROM usuarios LIMIT 1")
        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            return resultado[0]
        else:
            return "Usuario desconocido"
    except Exception as e:
        return f"Error al consultar la base de datos: {e}"

def Entregas():
    if st.button("Regresar"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

    # Encabezado
    col1, col2 = st.columns([1, 5])
    with col1:
        st.title("Entregas")
    with col2:
        st.image("GREENBRIERLOGO.png", width=100)

    st.text("Página de entregas. Por favor, genera los cierres, anéxalos y da clic en el botón.")

    archivo = st.file_uploader("Cargar archivo Excel", type=["xlsx", "xls"])

    if archivo is not None:
        try:
            df = pd.read_excel(archivo)
            st.success("Archivo cargado correctamente.")
            st.dataframe(df)

            nombre_usuario = obtener_usuario_desde_db()

            if st.button("Abrir Outlook con archivo adjunto"):
                try:
                    pythoncom.CoInitialize()

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                        tmp.write(archivo.getbuffer())
                        temp_path = tmp.name

                    outlook = win32com.client.Dispatch("Outlook.Application")
                    mail = outlook.CreateItem(0)
                    mail.To = "avisosgbrx@outlook.com"
                    mail.Subject = f"MRO INFORME {datetime.now().strftime('%Y-%m-%d')}"
                    mail.Body = f"Se adjunta el informe MRO en formato Excel.\n\nEnviado por: {nombre_usuario}"
                    mail.Attachments.Add(temp_path)
                    mail.Display()

                    st.success("Outlook se abrió con el correo preparado.")
                except Exception as e:
                    st.error(f"Por favor inicia sesión en Outlook: {e}")

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
