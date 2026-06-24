import streamlit as st
import pandas as pd

# 1. Forzamos el diseño ancho, pero Streamlit lo encogerá elegantemente en celular
st.set_page_config(page_title="Panel Móvil", layout="wide")

st.title("📊 Ocupación CDO")
st.write("Toca el menú de arriba a la izquierda (☰) en tu celular para ver los filtros.")

@st.cache_data
def cargar_datos():
    return pd.read_excel("datos.xlsx")

try:
    df = cargar_datos()

    # --- BARRA LATERAL (Se ocultará en celulares en un menú desplegable) ---
    st.sidebar.header("Filtros de Búsqueda")
    busqueda = st.sidebar.text_input("🔍 Buscar por texto:")

    columna_1 = 'CDO'
    columna_2 = 'DOMICILIO'

    df_filtrado = df.copy()

    if columna_1 in df.columns:
        opciones_1 = df[columna_1].dropna().unique()
        seleccion_1 = st.sidebar.multiselect(f"Filtrar por {columna_1}:", opciones_1, default=opciones_1)
        df_filtrado = df_filtrado[df_filtrado[columna_1].isin(seleccion_1)]

    if columna_2 in df.columns:
        opciones_2 = df[columna_2].dropna().unique()
        seleccion_2 = st.sidebar.multiselect(f"Filtrar por {columna_2}:", opciones_2, default=opciones_2)
        df_filtrado = df_filtrado[df_filtrado[columna_2].isin(seleccion_2)]

    if busqueda:
        df_filtrado = df_filtrado[df_filtrado.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]


    # --- DISEÑO ADAPTADO A CELULAR ---
    
    # Usamos una métrica limpia
    st.metric(label="Registros encontrados", value=len(df_filtrado))
    
    # Truco para celular: Agregamos un aviso amigable
    st.caption("💡 Truco: En el celular, arrastra la tabla hacia los lados para ver todas las columnas.")

    # Mostramos la tabla optimizada para pantallas táctiles
    st.dataframe(
        df_filtrado, 
        use_container_width=True,  # Se estira al 100% del ancho de la pantalla del celular
        hide_index=True            # Oculta el índice (0, 1, 2...) para ganar espacio horizontal en pantallas chicas
    )

except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'datos.xlsx'.")
except Exception as e:
    st.error(f"❌ Ocurrió un error: {e}")

# ... (Todo el código anterior de carga y filtros se mantiene igual) ...

    # --- SECCIÓN DE TABLA DINÁMICA ---
    st.subheader("📊 Resumen Ejecutivo (Tabla Dinámica)")

    if not df_filtrado.empty:
        # Creamos la tabla dinámica con Pandas
        # index: lo que va en las filas (ej: 'Zona')
        # columns: lo que va en las columnas (ej: 'Estado')
        # values: cualquier columna con datos para contar o sumar (ej: 'ID' o 'Nombre')
        # aggfunc: 'count' para contar registros, 'sum' para sumar valores numéricos
        
        try:
            tabla_dinamica = pd.pivot_table(
                df_filtrado, 
                index='CDO', 
                columns='DOMICILIO', 
                values=df.columns[0], # Usa la primera columna para contar
                aggfunc='count',
                fill_value=0 # Pone 0 si no hay datos en esa combinación
            ).reset_index() # Mantiene un formato limpio para Streamlit

            # Mostramos la tabla dinámica optimizada para celular
            st.dataframe(
                tabla_dinamica, 
                use_container_width=True,
                hide_index=True
            )
            
        except Exception as pivot_error:
            st.warning("Asegúrate de que las columnas 'CDO' y 'DOMICILIO' existan para armar la tabla dinámica.")

        # --- DETALLE COMPLETO (Opcional) ---
        # Si además de la dinámica querés ver el detalle fila por fila abajo:
        with st.expander("🔍 Ver detalle de registros individuales"):
            st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
            
    else:
        st.info("No hay datos que coincidan con los filtros seleccionados.")

except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'datos.xlsx'.")
