import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import platform
import altair as alt
import sqlite3

if platform.system() == "Windows":
    import win32com.client
    import pythoncom

def obtener_usuario_desde_db():
    try:
        conn = sqlite3.connect("Warehouse.db")
        cursor = conn.cursor()
        cursor.execute("SELECT usuario FROM usuarios LIMIT 1")
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else "Usuario no registrado"
    except sqlite3.Error as e:
        return f"Error al consultar la base de datos: {e}"

def cargar_archivo(archivo):
    extension = archivo.name.split(".")[-1].lower()
    try:
        if extension == "xlsx":
            return pd.read_excel(archivo, engine="openpyxl"), extension
        elif extension == "xls":
            return pd.read_excel(archivo, engine="xlrd"), extension
        elif extension == "csv":
            return pd.read_csv(archivo), extension
        else:
            return None, extension
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None, extension

def normalizar_columnas(columnas):
    return {col.lower().replace(" ", ""): col for col in columnas}

def enviar_correo_windows(archivo, extension, item_mas_popular, cantidad, nombre_usuario):
    try:
        pythoncom.CoInitialize()
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = "avisosgbrx@outlook.com"
        mail.Subject = f"MRO INFORME CIERRE TUNRO {datetime.now().strftime('%Y-%m-%d')}"
        mail.Body = f"Se adjunta el archivo original.\n\nÍtem más popular: {item_mas_popular} ({cantidad} entregas)\n\nEnviado por: {nombre_usuario}"

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extension}") as tmp:
            tmp.write(archivo.getbuffer())
            temp_path = tmp.name

        mail.Attachments.Add(temp_path)
        mail.Send()
        st.success("📧 Correo enviado automáticamente con el archivo original adjunto.")
    except Exception as e:
        st.error(f"No se pudo enviar el correo: {e}")

def Entregas():
    if platform.system() != "Windows":
        st.warning("⚠️ Esta sección es exclusiva para PC. Algunas funciones no están disponibles en dispositivos móviles.")

    if st.button("🔙 Regresar", key="regresar_entregas"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

    col1, col2 = st.columns([1, 5])
    with col1:
        st.title("Entregas")
    with col2:
        try:
            st.image("GREENBRIERLOGO.png", width=100)
        except:
            st.warning("Logo no encontrado.")

    st.text("Página de entregas. Por favor, genera los cierres, anéxalos y haz clic en el botón.")

    archivo = st.file_uploader("Cargar archivo", type=["xlsx", "xls", "csv"])

    if archivo is not None:
        df, extension = cargar_archivo(archivo)
        if df is None:
            st.error("Formato de archivo no soportado o error al leer el archivo.")
            return

        st.success("📦 Archivo cargado correctamente.")
        st.dataframe(df)

        columnas_map = normalizar_columnas(df.columns)
        if 'itemnumber' in columnas_map and 'quantity' in columnas_map:
            col_item = columnas_map['itemnumber']
            col_qty = columnas_map['quantity']

            conteo_items = df.groupby(col_item)[col_qty].sum().sort_values(ascending=False)
            item_mas_popular = conteo_items.idxmax()
            cantidad = conteo_items.max()
            st.success(f"🔔 El ítem más popular es '{item_mas_popular}' con {cantidad} entregas.")

            st.subheader("📊 Popularidad de ítems entregados")
            df_chart = conteo_items.head(10).reset_index()
            df_chart.columns = ['Artículo', 'Cantidad']
            chart = alt.Chart(df_chart).mark_bar().encode(
                x=alt.X('Artículo:N', sort='-y'),
                y='Cantidad:Q',
                color=alt.Color('Artículo:N', legend=None),
                tooltip=['Artículo', 'Cantidad']
            ).properties(
                width=600,
                height=400,
                title='Top 10 Artículos por Cantidad Entregada'
            )
            st.altair_chart(chart, use_container_width=True)

            nombre_usuario = obtener_usuario_desde_db()

            if platform.system() == "Windows":
                if st.button("📤 Enviar correo con archivo adjunto"):
                    enviar_correo_windows(archivo, extension, item_mas_popular, cantidad, nombre_usuario)
            else:
                st.warning("El envío automático de correos solo está disponible en Windows.")
        else:
            st.warning("El archivo debe contener las columnas 'Item Number' y 'Quantity'.")

Entregas()
