
#Código creado por Emiliano Castro: https://github.com/Humol-e 
#librerías
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import serial
import serial.tools.list_ports
import time
import plotly.express as px
from skimage import io
import toml
from st_paywall import add_auth
from toml.decoder import TomlDecodeError

st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.title("Visualización de datos.")
st.sidebar.header('Zona analítica `v1.0`')
st.sidebar.image("https://cdn.pixabay.com/photo/2019/08/06/22/48/artificial-intelligence-4389372_1280.jpg", use_column_width=True)
colu1, colu2 = st.columns(2)
tageo = st.empty()
@st.cache_resource 
def get_available_ports():
     ports = list(serial.tools.list_ports.comports())
     return [port.device for port in ports]

available_ports = get_available_ports()
with colu1:
    with st.popover("Selecciona el puerto COM"):
        st.write("Puertos disponibles :", available_ports)
        selected_port = st.selectbox("Selecciona el puerto COM", available_ports)

# Inicializar el DataFrame
valores = ["Temperatura", "Humedad", "Latitud", "Longitud", "Altitud", "Satélites","Tiempo", "VelocidadX", "VelocidadY", "AceleraciónX", "AceleraciónY", "AceleraciónZ", "Presión", "GiroscopioX", "GiroscopioY", "GiroscopioZ", "MagnetómetroX", "MagnetómetroY", "MagnetómetroZ"]

with colu2:
    with st.popover("Datos a procesar"):
        num_valores =len(valores)

        tageo = st.multiselect("Selecciona que datos vas a procesar.", valores, max_selections= num_valores)
df = pd.DataFrame(columns=tageo if tageo else valores)

# Filtrar el DataFrame basado en los tags seleccionados

df_filtrado = df[tageo]

start_button = st.button("Iniciar Lectura.")

dt = .25 #diferencia de tiempo entre cada lectura, usasdo para calcular la velocidad
velocidad = 0.0
velocidadx = 0.0
# Función para procesar una línea de datos del puerto serial

def procesar_linea_serial(linea):
    
    try:
        parts = linea.split('|')
        if len(parts) >= num_valores:  # Asegúrate de que haya suficientes datos
            datos = []
            for i in range(num_valores):
                if i < len(parts):
                    valor = float(parts[i].strip())
                    datos.append(valor)
                else:
                    datos.append(None)
            # Ahora `valores` contiene todos los valores procesados
              # 
            if "VelocidadX" in tageo and "VelocidadY" in tageo: 
                global velocidad, velocidadx
            #velocidad += mpuy_value *dt
            #velocidadx += mpux_value * dt
            return {
             i: datos[i] for i in range(num_valores)          }
        else:
            st.error(f"Datos incompletos recibidos del puerto serial: {linea}")
            return None
    except Exception as e:
        st.error(f"Error al procesar la línea de datos: {e}")
        return None
def convertir_claves(data, valores):
    return {valores[i]: data[i] for i in range(len(valores))}


# Función para leer datos en lotes
def leer_lote_serial(ser, lote_size=10):
    lineas = []
    for _ in range(lote_size):
        linea = ser.readline().decode('utf-8', errors='ignore').strip()
        if linea:
            lineas.append(linea)
    return lineas
miau = 1

colv1,colv2 = st.columns(2)
velocii = colv1.empty()
velocigraf = colv2.empty()
colx1,colx2 = st.columns(2)
velociix = colx1.empty()
tablatodo_placeholder = st.empty()
tablafiltro_placeholder = st.empty()
funciones_tag = {

    "velocigaugevhor" : ["Velocidad X", "General", "gauge"],
    "velocigaugevertical" : ["Velocidad Y", "General", "gauge"]
}
with st.sidebar:
    selected_tags = st.multiselect("Selecciona las gráficas a mostrar:", list(set(tag for tags in funciones_tag.values() for tag in tags)))


if miau == 0:
    with st.sidebar:
        add_auth(required=True)
        st.success('Gracias por tu login !')
    miau = 1

def mostrar_graficas(df, selected_tags):
    if "Velocidad X" in selected_tags:
        velocigaugehorizontal(df)  # Llama a la función para la gráfica de velocidad horizontal
    else:
        colx2.empty()  # Limpia la sección si no está seleccionada

    if "Velocidad Y" in selected_tags:
        velocigaugevertical(df)  # Llama a la función para la gráfica de velocidad vertical
    else:
        colv2.empty()  # Limpia la sección si no está seleccionada
def velocigaugevertical(df):
    veloz = df["VEL"].iloc[-1]

    figura = go.Figure(go.Indicator(   
        mode = "gauge+number",
        value = veloz,
        domain = {'x': [0,1], 'y': [0, 1]},
        title = {'text': "Velocidad vertical"},
        gauge = {'axis': {'range': [-100, 500]},
             'steps' : [
                 {'range': [-100, 100], 'color': "#e1f226"},
                 {'range': [101, 300], 'color': "#ff1818"},
                 {'range': [300, 450], 'color': "#660000"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))

    velocii.plotly_chart(figura)


def velocigaugehorizontal(df):
    veloz_x = df["VELX"].iloc[-1]

    figura = go.Figure(go.Indicator(
        mode="gauge+number",
        value=veloz_x,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Velocidad horizontal"},
        gauge={
            'axis': {'range': [-100, 500]},
            'steps': [
                {'range': [-100, 100], 'color': "#e1f226"},
                {'range': [101, 300], 'color': "#ff1818"},
                {'range': [300, 450], 'color': "#660000"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}
        }
    ))

    velociix.plotly_chart(figura)

def mostrar_tabla(df):

    tablatodo_placeholder.dataframe(df)

def mostrar_filtro(df_filtrado):
    tablafiltro_placeholder.dataframe(df_filtrado)

if  start_button:
    try:
        ser = serial.Serial(selected_port, 19200, timeout=1)

        while True:
            # Leer lote de líneas
            lineas = leer_lote_serial(ser, lote_size=5)
            for linea in lineas:
                data = procesar_linea_serial(linea)

                if data:
                    data = convertir_claves(data, valores)  # Convertir claves numéricas a cadenas
                    st.write(data)
                    new_row = pd.DataFrame(data, index=[0])
                    df = pd.concat([df, new_row], ignore_index=True)
                else :
                    st.error(f"Datos incompletos recibidos del puerto serial: {linea}")
            # Actualizar vista
            if not df_filtrado.empty:

                mostrar_filtro(df_filtrado)
                
            mostrar_tabla(df)

            mostrar_graficas(df,selected_tags)
            time.sleep(0.1)

    except serial.SerialException as e:
        st.error(f"Error al abrir el puerto {selected_port}: {e}")
    except PermissionError as e:
        st.error(f"Permiso denegado para abrir el puerto {selected_port}: {e}")
    except Exception as e:          
        st.error(f"Error inesperado: {e}")

else:
    st.warning("Por favor, selecciona un puerto COM disponible.")



