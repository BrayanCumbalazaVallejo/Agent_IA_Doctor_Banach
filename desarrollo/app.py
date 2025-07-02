#Herramientas
import numpy as np
import time
import os
import base64
from dotenv import load_dotenv
import pydicom
import io
#Visualización y parte gráfica
import matplotlib.pyplot as plt
import streamlit as st
#Manejo modelos de lenguaje
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

def cargar_pixeldata_dicom(carpeta_dicoms: str):
    """
    Genera un np array valores de gris de 3 dimensiones de la forma (axial,sagital,coronal) a partir de un directorio de dicoms
    """
    ordered_names = sorted(os.listdir(carpeta_dicoms))
    pixel_data = [pydicom.dcmread(os.path.join(carpeta_dicoms, name)).pixel_array for name in ordered_names] 
    return np.array(pixel_data,dtype="int16")

#Subir el API KEY para conectar con el modelo y dirección DICOM
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DICOM_FOLDER_PATH = os.getenv('DICOM_FOLDER_PATH')
#LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)
#Para poner ancha la página

st.set_page_config(layout="wide")

#Header decorado con la información del proyecto

col1_header, col2_header = st.columns(2)

with col1_header:
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

with col2_header:
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

#Cuerpo de la interfaz

col1, col2 = st.columns(2)
#Visualizador imagenes médicos
with col1:
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 1.2rem 1.5rem; border-radius: 10px; border: 1px solid #333;
                 display: flex; align-items: center; gap: 0.8rem; min-height: 80px;">
        <div style='font-size: 30px;'>🧠</div>
        <h2 style='color: #FFFFFF; margin: 0;'>
            <span style='color:#FF4B4B;'>Visualizador</span> de cortes
        </h2>
    </div>
    """, unsafe_allow_html=True)

    #Carga de datos
    @st.cache_data
    def cargar_datos():
        return cargar_pixeldata_dicom(DICOM_FOLDER_PATH)
    volumen = cargar_datos()

    #Selección Corte anátomicos
    cortes_anatomicos = {
        "Axial": volumen,
        "Coronal": volumen.transpose(1, 0, 2),
        "Sagital": volumen.transpose(2, 0, 1)
    }
    corte = st.radio("Tipo Corte anátomico", ["Axial", "Coronal", "Sagital"], horizontal=True)
    vol = cortes_anatomicos[corte]
    index = st.slider(f"Corte {corte.lower()}", 0, vol.shape[0] - 1, 0)
    #Rotación 
    grados_rotacion = st.slider("Rotar imagen (grados)", min_value=0, max_value=270, step=90, value=0)
    k = grados_rotacion // 90
    #Visualización en matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))
    slice_mostrar = np.rot90(vol[index], k=k)
    ax.imshow(slice_mostrar, cmap="gray")
    ax.axis("off")
    st.pyplot(fig)
    #Entrega de datos al modelo de lenguaje
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    st.session_state.current_dicom_image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)

#Chat con el modelo de lenguaje
with col2:
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
        #Contexto para darle al modelo sus indicaciones
        st.session_state.messages.append({
            "role": "system",
            "content": """
            Ahora eres el 'Doctor Banach'. Tu rol es ser un asistente médico virtual especializado en radiología.
            Tu principal objetivo es explicar los hallazgos en las imágenes médicas (como TAC o resonancias) de una manera extremadamente clara, sencilla y empática.
            Imagina que estás hablando con alguien que no tiene conocimientos médicos; usa analogías, evita la jerga compleja y, si debes usar un término técnico, explícalo inmediatamente de forma simple.
            Tu tono debe ser siempre tranquilizador, paciente y amable. Nunca reveles que eres un modelo de IA.
            Tu meta es que el usuario se sienta cómodo y comprenda la información que ve en la pantalla.
            """
        })


    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                if isinstance(msg["content"], list):
                    for item in msg["content"]:
                        if item["type"] == "text":
                            st.markdown(item["text"])
                else:
                    st.markdown(msg["content"])

    if prompt := st.chat_input("Escribe tu mensaje..."):
        with st.chat_message("user"):
            st.markdown(prompt)

        user_message_content = [{"type": "text", "text": prompt}]

        if st.session_state.get("current_dicom_image_base64"):
            #Entregarle la imagen al modelo de lenguaje
            user_message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{st.session_state.current_dicom_image_base64}"
                }
            })

        st.session_state.messages.append({"role": "user", "content": user_message_content})

        langchain_messages = []
        for msg in st.session_state.messages:
            if msg["role"] == "system":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        with st.spinner("El Doctor Banach está pensando..."):

            try:
                response = llm.invoke(langchain_messages).content
            except Exception as e:
                st.error(f"Error al comunicarse con Gemini: {e}")
                response = "Lo siento, hubo un error al procesar tu solicitud. Por favor, inténtalo de nuevo."

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})