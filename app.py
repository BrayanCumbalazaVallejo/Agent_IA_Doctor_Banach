import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time 
from dotenv import load_dotenv
#Funciones personalizadas
from my_functions import *

#Lógica
load_dotenv()

APIKEY = os.getenv('APIKEY')

#Inicio Interfaz
st.set_page_config(layout="wide")

#Header Interfaz
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 1.5rem; border-radius: 10px; border: 1px solid #333; height: 100%;">
        <div style='text-align: left; display: flex; flex-direction: column; justify-content: space-between; height: 100%;'>
            <div style='font-size: 50px;'>🩻 👨‍⚕️ 🧬 🩺</div>
            <h1 style='color: #FF4B4B; margin-bottom: 0.2em;'>
                <strong>Doctor</strong> <span style='color:#FFFFFF;'>Banach</span>
            </h1>
            <h4 style='color: #CCCCCC; margin-top: 0;'>Tu asistente de estudios de imágenes médicas</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 1.5rem; border-radius: 10px; border: 1px solid #333; height: 100%;">
        <h3 style="color: #FF4B4B; margin-bottom: 0.5rem;">📝 Descripción del proyecto</h3>
        <p style="color: #CCCCCC; font-size: 16px;">
            Esta herramienta interactiva permite visualizar <strong>cortes anatómicos</strong> (axial, coronal y sagital) 
            a partir de estudios médicos (como TAC o resonancias), y proporciona asistencia para la interpretación inicial de las imágenes.
        </p>
        <p style="color: #CCCCCC; font-size: 16px;">
            El objetivo es facilitar tanto el análisis técnico como el entendimiento por parte del paciente o especialista.
        </p>
        <ul style="color: #AAAAAA; font-size: 15px; line-height: 1.6;">
            <li>🔄 Visualización en tiempo real</li>
            <li>🔃 Rotación e inspección por cortes</li>
            <li>🧭 Soporte de diferentes vistas anatómicas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


st.divider()
#Cuerpo interfaz

col1, col2 = st.columns(2)
with col1:
    #Header de visualización dicom
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 1.2rem 1.5rem; border-radius: 10px; border: 1px solid #333;
                display: flex; align-items: center; gap: 0.8rem; min-height: 80px;">
        <div style='font-size: 30px;'>🧠</div>
        <h2 style='color: #FFFFFF; margin: 0;'>
            <span style='color:#FF4B4B;'>Visualizador</span> de cortes
        </h2>
    </div>
    """, unsafe_allow_html=True)

    #Cargar datos
    @st.cache_data
    def cargar_datos():
        return cargar_pixeldata_dicom("data\dataset_2_sub-01_run-01_T1w") #Ingrese ruta del dataset

    volumen = cargar_datos()

    cortes_anatomicos = {
        "Axial": volumen,
        "Coronal": volumen.transpose(1, 0, 2),
        "Sagital": volumen.transpose(2, 0, 1)
    }

    #Cortes anatomicos
    corte = st.radio("Tipo Corte anátomico", ["Axial", "Coronal", "Sagital"], horizontal=True)
    vol = cortes_anatomicos[corte]
    index = st.slider(f"Corte {corte.lower()}", 0, vol.shape[0] - 1, 0)

    #Rotación
    grados_rotacion = st.slider("Rotar imagen (grados)", min_value=0, max_value=270, step=90, value=0)
    k = grados_rotacion // 90  

    #Preparar visualización en matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))
    slice_mostrar = np.rot90(vol[index], k=k)
    ax.imshow(slice_mostrar, cmap="gray")
    ax.axis("off")

    #Desplegar
    st.pyplot(fig)


with col2:
    #Header chat
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 1.2rem 1.5rem; border-radius: 10px; border: 1px solid #333;
                display: flex; align-items: center; gap: 0.8rem; min-height: 80px;">
        <div style='font-size: 30px;'>💬</div>
        <h2 style='color: #FFFFFF; margin: 0;'>
            <span style='color:#FF4B4B;'>Asistencia</span> de Banach
        </h2>
    </div>
    """, unsafe_allow_html=True)
        
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if prompt := st.chat_input("Escribe tu mensaje..."):

        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})


        respuesta_falsa = "🤖 (Este es un chatbot simulado. La respuesta real se generaría aquí.)"


        with st.chat_message("assistant"):
            st.markdown(respuesta_falsa)

        st.session_state.messages.append({"role": "assistant", "content": respuesta_falsa})