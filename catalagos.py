import streamlit as st
import pandas as pd
import os
import platform

# Solo importar si estás en Windows
if platform.system() == "Windows":
    import pythoncom
    import win32com.client

def items():
    if st.button("🔙 Regresar"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

    # Encabezado
    col1, col2 = st.columns([1, 5])
    with col1:
        st.title("Catálogos")
    with col2:
        st.image("LOGO.jpeg", width=100)

    st.text("Hola, en este apartado puedes consultar los items de MRO.")
    st.subheader("Buscar por ID o palabra clave")

    # Diccionario de catálogos
    catalogos = {
        "MRO GRAL": "Catalogo de Ubi Mro GRAL JULIO 25.xlsx",
        "MRO GRAL ATRAS": "Catalogo bodega gral parte de atras..xlsx",
        "MRO GRAL SEGUNDO PISO": "Catalogo segundo piso..xlsx"
    }

    # Campo de búsqueda único
    filtro_id = st.text_input("🔍 Buscar por ID del ítem o palabra clave:")

    # Buscar en todos los catálogos
    if filtro_id:
        resultados_encontrados = False

        for nombre_visible, nombre_archivo in catalogos.items():
            ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)

            if os.path.exists(ruta_archivo):
                try:
                    df_catalogo = pd.read_excel(ruta_archivo)
                    df_filtrado = df_catalogo[df_catalogo.astype(str).apply(
                        lambda row: row.str.contains(filtro_id, case=False, na=False)
                    ).any(axis=1)]

                    if not df_filtrado.empty:
                        st.markdown(f"### 📁 Resultados en: **{nombre_visible}**")
                        st.dataframe(df_filtrado)
                        resultados_encontrados = True

                except Exception as e:
                    st.error(f"No se pudo abrir el catálogo: {nombre_archivo}")
                    st.exception(e)
            else:
                st.error(f"No se encontró el archivo: {nombre_archivo}")

        if not resultados_encontrados:
            st.warning("No se encontraron resultados en ningún catálogo.")
