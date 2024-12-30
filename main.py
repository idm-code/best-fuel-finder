import streamlit as st
import pandas as pd
import requests
import time

# Configuración de la página
st.set_page_config(page_title="Best Fuel Finder", page_icon="⛽", layout="wide")

@st.cache_data(show_spinner=False)
def get_gas_prices():
    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        estaciones = data.get('ListaEESSPrecio', [])
        
        # Utilizar List Comprehensions para mayor eficiencia
        datos = [
            {
                'Provincia': est['Provincia'],
                'Localidad': est['Localidad'],
                'Dirección': est['Dirección'],
                'Precio Gasolina 95 E5': float(est['Precio Gasolina 95 E5'].replace(',', '.')),
                'Precio Gasoleo A': float(est['Precio Gasoleo A'].replace(',', '.')),
                'Rótulo': est['Rótulo']
            }
            for est in estaciones
            if est['Precio Gasolina 95 E5'] and est['Precio Gasoleo A']
        ]
        df = pd.DataFrame(datos)
        end_time = time.time()
        print(f"Tiempo de carga: {end_time - start_time:.2f} segundos")
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error en la solicitud de la API: {e}")
        return pd.DataFrame()
    except ValueError as ve:
        st.error(f"Error al procesar los datos: {ve}")
        return pd.DataFrame()

def main():
    # Obtener los datos con un spinner para mejor experiencia de usuario
    with st.spinner('Cargando datos...'):
        df = get_gas_prices()

    if df.empty:
        st.error("No se han podido obtener los datos.")
        return

    # Título centrado
    st.markdown("<h1 style='text-align: center;'>Precios de los carburantes en España</h1>", unsafe_allow_html=True)

    # Filtro por provincia
    provincias = ["Todas"] + sorted(df['Provincia'].unique())
    provincia_seleccionada = st.selectbox("Seleccionar provincia:", options=provincias)

    if provincia_seleccionada != "Todas":
        df = df[df['Provincia'] == provincia_seleccionada]

    # Mostrar una muestra inicial para reducir el tiempo de renderizado
    mostrar_todo = st.checkbox("Mostrar todos los registros")
    if not mostrar_todo:
        df = df.head(500)  # Ajusta este número según tus necesidades

    # Tiempo de renderizado
    render_start = time.time()

    # Mostrar el DataFrame interactivo
    st.dataframe(df, use_container_width=True)

    render_end = time.time()
    st.write(f"Tiempo de renderizado: {render_end - render_start:.2f} segundos")

if __name__ == "__main__":
        main()