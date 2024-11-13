import streamlit as st
import pandas as pd

def cargar_archivo(archivo):
    """Carga un archivo CSV o TSV."""
    try:
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
        elif archivo.name.endswith(".tsv"):
            df = pd.read_csv(archivo, sep='\t')
        else:
            st.error("El archivo debe ser un CSV o TSV.")
            return None
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

def calcular_cuartiles(df, columna):
    try:
        Q1 = df[columna].quantile(0.25)
        Q2 = df[columna].median()
        Q3 = df[columna].quantile(0.75)
        Q4 = df[columna].max()

        nombre_nueva_columna = f"{columna}_cuartil"

        def asignar_cuartil(valor):
            if valor <= Q1:
                return "1"
            elif valor <= Q2:
                return "2"
            elif valor <= Q3:
                return "3"
            elif valor <= Q4:
                return "4"
        
        # New column
        df[nombre_nueva_columna] = df[columna].apply(asignar_cuartil)
        # two value return
        return {"Q1": Q1, "Q2 (Mediana)": Q2, "Q3": Q3, "Q4": Q4}, df
    
    except KeyError:
        st.error(f"La columna '{columna}' no existe en el DataFrame.")
        return None, df

def agrupacion_personalizada(df, columna, metodo_agrupacion):
    """Agrupa los datos según el método seleccionado por el usuario."""
    try:
        if metodo_agrupacion == "Suma":
            return df.groupby(columna).sum()
        elif metodo_agrupacion == "Media":
            return df.groupby(columna).mean()
        elif metodo_agrupacion == "Conteo":
            return df.groupby(columna).count()
        else:
            st.error("Método de agrupación no válido.")
            return None
    except Exception as e:
        st.error(f"Error en la agrupación: {e}")
        return None



















def app():
    st.set_page_config(page_title="Análisis de Datos")
    st.title("Cargador de Archivo y Análisis de Datos")


    archivo = st.file_uploader("Sube tu archivo CSV o TSV", type=["csv", "tsv"])


    if archivo is not None:
        if "df_original" not in st.session_state:
            df = cargar_archivo(archivo)
            if df is not None:
                st.session_state["df_original"] = df
                st.session_state["df_modificado"] = df.copy()  


    if "df_modificado" in st.session_state:
        st.write("Datos cargados:")
        st.write(st.session_state["df_modificado"].head())

        st.write("### Opciones de Análisis")


        if st.checkbox("Calcular Cuartiles"):
            columna_cuartiles = st.selectbox("Selecciona una columna para calcular cuartiles:", st.session_state["df_modificado"].columns)
            if st.button("Calcular Cuartiles"):
                cuartiles, df_actualizado = calcular_cuartiles(st.session_state["df_modificado"], columna_cuartiles)
                if cuartiles:
                    st.session_state["df_modificado"] = df_actualizado  # Guardar cambios en el DataFrame modificado
                    st.write("Cuartiles calculados:")
                    st.write(cuartiles)

        # Seleccionar y hacer agrupación
        if st.checkbox("Realizar Agrupación"):
            columna_agrupacion = st.selectbox("Selecciona una columna para agrupar:", st.session_state["df_modificado"].columns)
            metodo_agrupacion = st.selectbox("Selecciona el método de agrupación:", ["Suma", "Media", "Conteo"])
            if st.button("Agrupar"):
                df_agrupado = agrupacion_personalizada(st.session_state["df_modificado"], columna_agrupacion, metodo_agrupacion)
                if df_agrupado is not None:
                    st.session_state["df_modificado"] = df_agrupado  # Guardar la agrupación en el DataFrame modificado
                    st.write("Resultado de la agrupación:")
                    st.write(st.session_state["df_modificado"])

        # Mostrar el DataFrame actualizado con las columnas y cambios añadidos
        st.write("### DataFrame Actualizado")
        st.write(st.session_state["df_modificado"])

        # Opción para descargar el DataFrame modificado como CSV
        st.write("### Descargar DataFrame Modificado")
        csv = st.session_state["df_modificado"].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar como CSV",
            data=csv,
            file_name="data_modificada.csv",
            mime="text/csv",
        )

# # Ejecutar la aplicación
# if __name__ == "__main__":
#     app()

