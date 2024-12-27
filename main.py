import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Best Fuel Finder", page_icon="⛽", layout="wide")

def get_gas_prices():
    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['ListaEESSPrecio']
    else:
        return "Error al obtener los datos"
    
def main():
    api = get_gas_prices()

    datos = []
    for i in api:
        datos.append([i['Provincia'], i['Localidad'], i['Dirección'], i['Precio Gasolina 95 E5'], i['Precio Gasoleo A']])
    df = pd.DataFrame(datos, columns=['Provincia', 'Localidad' ,'Dirección', 'Precio Gasolina 95 E5', 'Precio Gasoleo A'])

    st.title("Precios de los carburantes en España")
    st.write(df)


if __name__ == "__main__":
    main()