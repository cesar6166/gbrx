import streamlit as st
import pandas as pd
import os
import platform

if platform.system() == "Windows":
    import pythoncom
    import win32com.client

def buscar_en_catalogo(nombre_archivo, filtro):
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    if not os.path.exists(ruta):
        return None, f"❌ Archivo no encontrado: {nombre_archivo}"

    try:
        df = pd.read_excel(ruta)
        if df.empty:
            return None, f"⚠️ El archivo está vacío: {nombre_archivo}"

        df_filtrado = df[df.astype(str).apply(
            lambda row: row.str.contains(filtro, case=False, na=False)
        ).any(axis=1)]

        if df_filtrado.empty:
            return None, None  # No resultados, pero sin error
        return df_filtrado, None

    except Exception as e:
        return None, f"❌ Error al abrir el archivo {nombre_archivo}: {e}"

def items():
    if st.button("🔙 Regresar"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

    col1, col2 = st.columns([1, 5])
    with col1:
        st.title("Catálogos")
    with col2:
        try:
            st.image("LOGO.jpeg", width=100)
        except:
            st.warning("No se pudo cargar el logo.")

    st.text("Hola, en este apartado puedes consultar los items de MRO.")
    st.subheader("Buscar por ID o palabra clave")

    catalogos = {
        "MRO GRAL": "Catalogo de Ubi Mro GRAL JULIO 25.xlsx",
        "MRO GRAL ATRAS": "Catalogo bodega gral parte de atras..xlsx",
        "MRO GRAL SEGUNDO PISO": "Catalogo segundo piso..xlsx"
    }

    filtro_id = st.text_input("🔍 Buscar por ID del ítem o palabra clave:")

    if filtro_id:
        resultados_encontrados = False

        for nombre_visible, nombre_archivo in catalogos.items():
            df_resultado, error = buscar_en_catalogo(nombre_archivo, filtro_id)

            if error:
                st.error(error)
            elif df_resultado is not None:
                st.markdown(f"### 📁 Resultados en: **{nombre_visible}**")
                st.dataframe(df_resultado)
                resultados_encontrados = True

        if not resultados_encontrados:
            st.warning("🔎 No se encontraron resultados en ningún catálogo.")

items()

