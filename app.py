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
                index='Zona', 
                columns='Estado', 
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
            st.warning("Asegúrate de que las columnas 'Zona' y 'Estado' existan para armar la tabla dinámica.")

        # --- DETALLE COMPLETO (Opcional) ---
        # Si además de la dinámica querés ver el detalle fila por fila abajo:
        with st.expander("🔍 Ver detalle de registros individuales"):
            st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
            
    else:
        st.info("No hay datos que coincidan con los filtros seleccionados.")

except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'datos.xlsx'.")