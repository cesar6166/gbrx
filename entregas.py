import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import sqlite3
import platform
import io
import xlsxwriter

# Solo importar si estamos en Windows
if platform.system() == "Windows":
    import win32com.client
    import pythoncom

# Función para obtener el nombre del usuario desde la base de datos
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

# Función principal de entregas
def Entregas():
    if platform.system() != "Windows":
        st.warning("⚠️ Esta sección es exclusiva para PC. Algunas funciones no están disponibles en dispositivos móviles.")

    if st.button("Regresar"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

    col1, col2 = st.columns([1, 5])
    with col1:
        st.title("Entregas")
    with col2:
        st.image("GREENBRIERLOGO.png", width=100)

    st.text("Página de entregas. Por favor, genera los cierres, anéxalos y haz clic en el botón.")

    archivo = st.file_uploader("Cargar archivo", type=["xlsx", "xls", "csv"])

    if archivo is not None:
        try:
            extension = archivo.name.split(".")[-1].lower()

            if extension in ["xlsx", "xls"]:
                df = pd.read_excel(archivo, engine="openpyxl" if extension == "xlsx" else "xlrd")
            elif extension == "csv":
                df = pd.read_csv(archivo)
            else:
                st.error("Formato de archivo no soportado.")
                return

            st.success("Archivo cargado correctamente.")
            st.dataframe(df)

            # Detectar automáticamente la columna de ítems
            columnas_excluir = ['id', 'codigo', 'iditem', 'código']
            columnas_preferidas = ['nombre', 'descripción', 'artículo', 'producto','descripcion']

            columnas_normalizadas = {col.lower(): col for col in df.columns}
            columna_item = None

            for preferida in columnas_preferidas:
                if preferida in columnas_normalizadas and columnas_normalizadas[preferida].lower() not in columnas_excluir:
                    columna_item = columnas_normalizadas[preferida]
                    break

            if not columna_item:
                for col in df.columns:
                    if df[col].dtype == object and df[col].nunique() < len(df) * 0.9:
                        if col.lower() not in columnas_excluir:
                            columna_item = col
                            break

            if columna_item:
                conteo_items = df[columna_item].value_counts()
                item_mas_popular = conteo_items.idxmax()
                cantidad = conteo_items.max()
                st.toast(f"🔔 El ítem más popular es '{item_mas_popular}' con {cantidad} entregas.")
                st.subheader("📊 Popularidad de ítems entregados")
                st.bar_chart(conteo_items.head(10))

                # Crear reporte Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    conteo_items.to_frame(name='Cantidad').to_excel(writer, sheet_name='Conteo Total')
                    conteo_items.head(10).to_frame(name='Cantidad').to_excel(writer, sheet_name='Top 10 Más Entregados')
                output.seek(0)

                # Obtener nombre de usuario
                nombre_usuario = obtener_usuario_desde_db()

                # Enviar correo automáticamente
                if platform.system() == "Windows":
                    try:
                        pythoncom.CoInitialize()
                        outlook = win32com.client.Dispatch("Outlook.Application")
                        mail = outlook.CreateItem(0)
                        mail.To = "avisosgbrx@outlook.com"
                        mail.Subject = f"MRO INFORME {datetime.now().strftime('%Y-%m-%d')}"
                        mail.Body = f"Se adjunta el informe MRO.\n\nÍtem más popular: {item_mas_popular} ({cantidad} entregas)\n\nEnviado por: {nombre_usuario}"

                        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                            tmp.write(output.read())
                            temp_path = tmp.name

                        mail.Attachments.Add(temp_path)
                        mail.Send()
                        st.success("📧 Correo enviado automáticamente con el reporte adjunto.")
                    except Exception as e:
                        st.error(f"No se pudo enviar el correo: {e}")
                else:
                    st.warning("El envío automático de correos solo está disponible en Windows.")

            else:
                st.warning("No se pudo detectar automáticamente la columna de ítems.")

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

