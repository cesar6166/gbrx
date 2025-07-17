import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import sqlite3
import platform
import urllib.parse
import csv  # Para detectar delimitadores
import streamlit.components.v1 as components

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

    archivo = st.file_uploader("Cargar archivo", type=["xlsx", "xls", "csv", "txt"])

    if archivo is not None:
        try:
            if archivo.name.endswith((".xlsx", ".xls")):
                df = pd.read_excel(archivo)
            elif archivo.name.endswith((".csv", ".txt")):
                sample = archivo.read(2048).decode("utf-8")
                archivo.seek(0)
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample)
                delimiter_detectado = dialect.delimiter
                df = pd.read_csv(archivo, delimiter=delimiter_detectado)
                st.info(f"Delimitador detectado: '{delimiter_detectado}'")
            else:
                st.error("Formato de archivo no soportado.")
                return

            st.success("Archivo cargado correctamente.")
            st.dataframe(df)

            nombre_usuario = obtener_usuario_desde_db()
            asunto = f"MRO INFORME {datetime.now().strftime('%Y-%m-%d')}"
            cuerpo = f"Se adjunta el informe MRO.\n\nEnviado por: {nombre_usuario}"
            mailto_link = f"mailto:avisosgbrx@outlook.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"

            # Selección del entorno
            modo_envio = st.radio("¿Desde dónde estás usando esta app?", ["PC con Outlook", "Celular o sin Outlook"])

            if modo_envio == "Celular o sin Outlook":
                st.markdown(f"[📧 Abrir correo en tu celular, unsafe_allow_html=True)

            elif modo_envio == "PC con Outlook":
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
