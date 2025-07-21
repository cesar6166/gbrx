import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import tempfile
import platform

def generar_reporte_popularidad(df):
    # Detectar automáticamente la columna de ítems
    posibles_columnas = ['Nombre', 'Descripción', 'Artículo', 'Producto', 'Item', 'Nombre del ítem']
    columnas_normalizadas = {col.lower(): col for col in df.columns}
    columna_item = None

    for posible in posibles_columnas:
        if posible.lower() in columnas_normalizadas:
            columna_item = columnas_normalizadas[posible.lower()]
            break

    # Si no se encuentra por nombre, usar heurística
    if not columna_item:
        for col in df.columns:
            if df[col].dtype == object and df[col].nunique() < len(df) * 0.9:
                columna_item = col
                break

    if not columna_item:
        return None, None, None

    conteo_items = df[columna_item].value_counts()
    item_mas_popular = conteo_items.idxmax()
    cantidad = conteo_items.max()

    # Crear archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        conteo_items.to_frame(name='Cantidad').to_excel(writer, sheet_name='Conteo Total')
        conteo_items.head(10).to_frame(name='Cantidad').to_excel(writer, sheet_name='Top 10 Más Entregados')
    output.seek(0)

    return output, item_mas_popular, cantidad

# Simulación de carga de archivo y procesamiento
archivo = st.file_uploader("Cargar archivo de entregas", type=["xlsx", "xls", "csv"])

if archivo is not None:
    extension = archivo.name.split(".")[-1].lower()
    try:
        if extension in ["xlsx"]:
            df = pd.read_excel(archivo, engine='openpyxl')
        elif extension in ["xls"]:
            df = pd.read_excel(archivo, engine='xlrd')
        elif extension == "csv":
            df = pd.read_csv(archivo)
        else:
            st.error("Formato de archivo no soportado.")
            st.stop()

        st.success("Archivo cargado correctamente.")
        st.dataframe(df)

        reporte, item_popular, cantidad = generar_reporte_popularidad(df)

        if reporte:
            st.toast(f"🔔 El ítem más popular es '{item_popular}' con {cantidad} entregas.")
            st.subheader("📊 Popularidad de ítems entregados")
            st.bar_chart(df[item_popular].value_counts().head(10))

            st.download_button(
                label="📥 Descargar reporte de popularidad",
                data=reporte,
                file_name=f"reporte_popularidad_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No se pudo detectar automáticamente la columna de ítems.")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

