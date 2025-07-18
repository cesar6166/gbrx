import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import sqlite3
import platform

# Solo importar si estamos en Windows
if platform.system() == "Windows":
    import win32com.client
    import pythoncom
else:
    import requests  # Para usar Microsoft Graph API o SMTP en la nube

def obtener_usuario_desde_db():
    try:
        conn = sqlite3.connect("Warehouse.db")
        cursor = conn.cursor()
        cursor.execute("SELECT usuario FROM usuarios LIMIT 1")
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else "Usuario desconocido"
    except Exception as e:
        return f"Error al consultar la base de datos: {e}"

def Entregas():
    # Mostrar advertencia si no es Windows
    if platform.system() != "Windows":
        st.warning("⚠️ Esta sección es exclusiva para uso desde una PC. Algunas funciones no estan disponibles para celulares.")

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

            if st.button("Enviar correo con archivo adjunto"):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                        tmp.write(archivo.getbuffer())
                        temp_path = tmp.name

                    if platform.system() == "Windows":
                        pythoncom.CoInitialize()
                        outlook = win32com.client.Dispatch("Outlook.Application")
                        mail = outlook.CreateItem(0)
                        mail.To = "avisosgbrx@outlook.com"
                        mail.Subject = f"MRO INFORME {datetime.now().strftime('%Y-%m-%d')}"
                        mail.Body = f"Se adjunta el informe MRO en formato Excel.\n\nEnviado por: {nombre_usuario}"
                        mail.Attachments.Add(temp_path)
                        mail.Display()
                        st.success("Outlook se abrió con el correo preparado.")
                    else:
                        st.warning("No disponible")
                        # Aquí puedes integrar Microsoft Graph API o SMTP
                        # Puedo ayudarte a implementarlo si ya tienes las credenciales

                except Exception as e:
                    st.error(f"No se pudo preparar el correo: {e}")

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
