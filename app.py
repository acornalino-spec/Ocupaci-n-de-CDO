import streamlit as st
import pandas as pd

# Configuración de la página (opcional, para que se vea ancha)
st.set_page_config(page_title="Visualizador de Datos", layout="wide")

st.title("📊 Mi Panel de Control de Excel")
st.write("Filtra la información del archivo de forma dinámica.")

# 1. Cargar el archivo Excel de forma eficiente
@st.cache_data
def cargar_datos():
    # Reemplaza 'datos.xlsx' por el nombre exacto de tu archivo
    return pd.read_excel("datos.xlsx")

try:
    df = cargar_datos()

    # --- SECCIÓN DE FILTROS (En la barra lateral) ---
    st.sidebar.header("Filtros disponibles")

    # Filtro 1: Buscador de texto libre (busca en todas las columnas)
    busqueda = st.sidebar.text_input("🔍 Buscar por texto:")

    # Filtro 2: Desplegable múltiple (asumiendo que tenés una columna llamada 'Categoría')
    # Cambia 'Categoría' por el nombre real de alguna columna de tu Excel (ej: 'Zona', 'Tipo', 'Estado')
    columna_filtro = 'Categoría' 
    
    if columna_filtro in df.columns:
        opciones = df[columna_filtro].dropna().unique()
        seleccion = st.sidebar.multiselect(f"Filtrar por {columna_filtro}:", opciones, default=opciones)
        # Aplicamos el filtro de categoría
        df_filtrado = df[df[columna_filtro].isin(seleccion)]
    else:
        df_filtrado = df.copy()

    # Aplicamos el filtro de búsqueda de texto si el usuario escribió algo
    if busqueda:
        # Esto busca el texto en cualquier celda de la fila
        df_filtrado = df_filtrado[df_filtrado.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]

    # --- SECCIÓN DE RESULTADOS ---
    # Mostramos la cantidad de registros encontrados
    st.metric(label="Registros encontrados", value=len(df_filtrado))

    # Mostramos la tabla interactiva
    st.dataframe(df_filtrado, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'datos.xlsx'. Asegúrate de subirlo al mismo repositorio de GitHub.")
except Exception as e:
    st.error(f"❌ Ocurrió un error al procesar el Excel: {e}")