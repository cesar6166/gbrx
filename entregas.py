import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import sqlite3
import platform
import urllib.parse
import csv
import io

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
                df = pd.read_excel(archivo, engine="openpyxl" if archivo.name.endswith(".xlsx") else "xlrd")
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

            modo_envio = st.radio("¿Desde dónde estás usando esta app?", ["PC o celular"])

            # Guardar archivo como Excel para descarga
            output = io.BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="📥 Descargar archivo Excel",
                data=output,
                file_name=f"MRO_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.markdown(f"📧 Abrir correo para enviar informe", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
