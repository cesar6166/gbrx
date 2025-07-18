import streamlit as st
import pandas as pd
from datetime import datetime
import platform 
import os

# Solo importar si estás en Windows
if platform.system() == "Windows":
    import pythoncom
    import win32com.client

def items():
    if st.button("Regresar"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

    st.title("Catálogos")
    st.text("Hola, en este apartado puedes consultar los catálogos de MRO.")

    st.subheader("Selecciona la ubicación del almacén")

    # Inicializar variable para el DataFrame
    df_catalogo = None

    # Checkbox para MRO GRAL
    if st.checkbox("MRO GRAL"):
        nombre_archivo = "Catalogo de Ubi Mro GRAL JULIO 25.xlsx"
        ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)

        if os.path.exists(ruta_archivo):
            try:
                df_catalogo = pd.read_excel(ruta_archivo)
                st.success(f"Catálogo '{nombre_archivo}' cargado correctamente.")
            except Exception as e:
                st.error("No se pudo abrir el catálogo.")
                st.exception(e)
        else:
            st.error(f"No se encontró el archivo: {nombre_archivo}")

    # Si el catálogo fue cargado, mostrar campo de búsqueda
    if df_catalogo is not None:
        filtro_id = st.text_input("🔍 Buscar por ID del ítem o palabra clave:")

        if filtro_id:
            df_filtrado = df_catalogo[df_catalogo.astype(str).apply(
                lambda row: row.str.contains(filtro_id, case=False, na=False)
            ).any(axis=1)]

            if not df_filtrado.empty:
                st.dataframe(df_filtrado)
            else:
                st.warning("No se encontraron resultados con ese valor.")
        else:
            st.dataframe(df_catalogo)
