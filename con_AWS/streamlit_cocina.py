import streamlit as st
import requests
import json
import base64
from requests.utils import quote

# Función para convertir imagen a base64 (necesario para CSS)
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Función para establecer el fondo
def set_background(jpg_file):
    bin_str = get_base64(jpg_file) 
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed; 
    }
    </style>
    ''' % bin_str 
    st.markdown(page_bg_img, unsafe_allow_html=True)

# --- Configuración de la página ---
st.set_page_config(layout="wide") 

# Establecer imagen de fondo (reemplaza 'fondo.jpg' con tu archivo)
set_background('img/gorro.jpg')  

if "show_history" not in st.session_state:          # CAMBIO
    st.session_state.show_history = True             # CAMBIO

if "pregunta_guardada" not in st.session_state:     # CAMBIO
    st.session_state.pregunta_guardada = ""          # CAMBIO
if "respuesta_guardada" not in st.session_state:     # CAMBIO
    st.session_state.respuesta_guardada = ""         # CAMBIO

def toggle_history():                                 # CAMBIO
    st.session_state.show_history = not st.session_state.show_history  # CAMBIO

# Configuración
API_URL = "http://localhost:5000" 
st.set_page_config(page_title="Tu asistente de Cocina 🍳", layout="wide")

# Diseño de la interfaz
st.title("🍳 ChefAI Tu asistente de Cocina")
st.markdown("Pregunta lo que quieras sobre técnicas, recetas o ingredientes:")

# Dividir input en columnas para controlar el ancho
col_input, col_empty = st.columns([6,6])  # mitad y mitad

with col_input:
    pregunta = st.text_input("Escribe tu pregunta:", placeholder="Ej: ¿Cómo hacer un risotto?")

with col_empty:
    st.write("")  # espacio vacío

if st.button("Obtener respuesta"):
    if pregunta:
        try:
            pregunta_codificada = quote(pregunta)           # CAMBIO
            response = requests.get(f"{API_URL}/pront/{pregunta_codificada}")  # CAMBIO
            
            if response.status_code == 200:
                respuesta = response.json().get("respuesta", "Sin respuesta")
                st.session_state.pregunta_guardada = pregunta   # CAMBIO
                st.session_state.respuesta_guardada = respuesta # CAMBIO
                        
            elif response.status_code == 400:
                st.error("⚠️ Por favor, haz preguntas solo sobre cocina.")
            else:
                st.error(f"Error inesperado: {response.text}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"❌ No se pudo conectar a la API: {str(e)}")
    else:
        st.warning("Por favor, escribe una pregunta.")

if st.session_state.respuesta_guardada:
    col1, col2 = st.columns([7, 5])

    with col1:
        st.success("**Respuesta:**")
        st.markdown(f"> {st.session_state.respuesta_guardada}")  # CAMBIO

    with col2:
        st.button("Mostrar/Ocultar historial", on_click=toggle_history)  # CAMBIO

        if st.session_state.show_history:  # CAMBIO
            st.markdown("### 🕘 Historial de consultas")
            try:
                historial = requests.get(f"{API_URL}/historial").json()
                for item in historial.get("historial", [])[:5]:
                    st.caption(f"📌 **Pregunta:** {item['pregunta']}")
                    st.text(f"💬 Respuesta: {item['respuesta']}")
                    st.caption(f"📅 Fecha: {item['fecha']}")
                    st.divider()
            except requests.exceptions.RequestException as e:
                st.error(f"Error al cargar el historial: {str(e)}")