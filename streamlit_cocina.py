import streamlit as st
import requests
import json
import base64

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

# Configuración
API_URL = "http://localhost:5000" 
st.set_page_config(page_title="Tu asistente de Cocina 🍳", layout="wide")

# Diseño de la interfaz
st.title("🍳 Tu asistente de Cocina")
st.markdown("Pregunta lo que quieras sobre técnicas, recetas o ingredientes:")

# Input del usuario
pregunta = st.text_input("Escribe tu pregunta:", placeholder="Ej: ¿Cómo hacer un risotto?")

if st.button("Obtener respuesta"):
    if pregunta:
        try:
            # Llama a tu API Flask
            response = requests.get(f"{API_URL}/pront/{pregunta}")
            
            if response.status_code == 200:
                respuesta = response.json().get("respuesta", "Sin respuesta")
                st.success("**Respuesta:**")
                st.markdown(f"> {respuesta}")
                
                # Opcional: Mostrar historial de la API
                with st.expander("Ver historial de consultas"):
                    historial = requests.get(f"{API_URL}/historial").json()
                    for item in historial.get("historial", [])[:5]:  # Muestra las últimas 5
                        st.caption(f"**Pregunta:** {item[0]}")
                        st.text(f"Respuesta: {item[1]}")
                        st.divider()
                        
            elif response.status_code == 400:
                st.error("⚠️ Por favor, haz preguntas solo sobre cocina.")
            else:
                st.error(f"Error inesperado: {response.text}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"❌ No se pudo conectar a la API: {str(e)}")
    else:
        st.warning("Por favor, escribe una pregunta.")