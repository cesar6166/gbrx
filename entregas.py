import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import sqlite3
import platform
import urllib.parse  # Para codificar el enlace mailto

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

            # Enlace mailto para abrir correo desde el celular
            asunto = f"MRO INFORME {datetime.now().strftime('%Y-%m-%d')}"
            cuerpo = f"Se adjunta el informe MRO en formato Excel.\n\nEnviado por: {nombre_usuario}"
            mailto_link = f"mailto:avisosgbrx@outlook.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
            st.markdown(f"📧 Abrir correo en tu celular", unsafe_allow_html=True)

            if st.button("Abrir Outlook con archivo adjunto"):
                try:
                    if platform.system() == "Windows":
                        import pythoncom
                        import win32com.client

                        pythoncom.CoInitialize()

                        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                            tmp.write(archivo.getbuffer())
                            temp_path = tmp.name

                        outlook = win32com.client.Dispatch("Outlook.Application")
                        mail = outlook.CreateItem(0)
                        mail.To = "avisosgbrx@outlook.com"
                        mail.Subject = asunto
                        mail.Body = cuerpo
                        mail.Attachments.Add(temp_path)
                        mail.Display()

                        st.success("Outlook se abrió con el correo preparado.")
                    else:
                        st.warning("Estás en un entorno que no soporta Outlook local. Usa el enlace de arriba para enviar el correo desde tu celular.")
                except Exception as e:
                    st.error(f"No se pudo preparar el correo: {e}")

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
