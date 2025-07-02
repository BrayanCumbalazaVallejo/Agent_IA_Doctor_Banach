import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import initialize_agent, Tool, AgentType
import base64
import io

from my_functions import *

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)
# Agente 1 encargado de analizar los datos y la imagen del paciente para luego dar un analisis de ello
agente_doctor = initialize_agent(
    tools=[],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
# agente 2 revisa lo proporcionado por el agente 1 para corregir posibles alucionaciones por parte del agente
llm_2 = ChatGoogleGenerativeAI(temperature=0)
agente_corrector = initialize_agent(
    tools=[],
    llm=llm_2,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
st.set_page_config(layout="wide")

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

col1, col2 = st.columns(2)

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

    @st.cache_data
    def cargar_datos():
        return cargar_pixeldata_dicom("data/dataset_2_sub-01_run-01_T1w")

    volumen = cargar_datos()

    cortes_anatomicos = {
        "Axial": volumen,
        "Coronal": volumen.transpose(1, 0, 2),
        "Sagital": volumen.transpose(2, 0, 1)
    }

    corte = st.radio("Tipo Corte anátomico", ["Axial", "Coronal", "Sagital"], horizontal=True)
    vol = cortes_anatomicos[corte]
    index = st.slider(f"Corte {corte.lower()}", 0, vol.shape[0] - 1, 0)

    grados_rotacion = st.slider("Rotar imagen (grados)", min_value=0, max_value=270, step=90, value=0)
    k = grados_rotacion // 90

    fig, ax = plt.subplots(figsize=(6, 6))
    slice_mostrar = np.rot90(vol[index], k=k)
    ax.imshow(slice_mostrar, cmap="gray")
    ax.axis("off")

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    st.session_state.current_dicom_image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)

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
        # --- INICIO DE LA CORRECCIÓN ---
        # Mensaje de sistema mejorado para dar contexto al Doctor Banach.
        st.session_state.messages.append({
            "role": "system",
            "content": """           
                Eres el Doctor Banach, un asistente médico virtual especializado en radiología. Tu misión es:
                
                1. Orientación de la imagen  
                   Describe siempre la vista (axial, coronal, sagital) y la ventana (hueso/tejido blando) antes de los hallazgos.
                2. Hallazgos principales  
                     Breve descripción del hallazgo  
                     Ubicación anatómica precisa 
                3. Diagnósticos diferenciales  
                     Ofrece hasta 2 posibles causas y su probabilidad relativa.
                
                4. Siguiente paso sugerido
                     Indica un examen o consulta recomendada 
                5. Interacción  
                   “Si quieres que ampliemos o comparemos con otro corte, indícalo.”
                6. Analogías y tono 
                   Usa analogías sencillas y explica todo término técnico.
                   Tono tranquilizador, empático y siempre recuerda: esto no reemplaza la opinión del radiólogo humano.
                Recuerda: no reveles que eres una IA. Asegúrate de que el usuario se sienta cómodo y comprenda cada paso.
                condicionales:
                
                si es un paciente, usa lenguaje muy sencillo, sin tecnicismos.
                si es medico o estudiante de medicina o carrera afin puedes usar lenguaje medico, pero explica terminos complejos de ser necesario.
                Cuando no se proporcionen sintomas, no inventes informacion clinica
                Cuando se proporcionen sintomas, intenta vincular los hallazgos con los sintomas mencionados
                """
        })
        # --- FIN DE LA CORRECCIÓN ---

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

        # --- INICIO DE LA CORRECCIÓN ---
        # Se actualiza el mensaje del spinner para mayor consistencia.
        with st.spinner("El Doctor Banach está pensando..."):
            try:
                # Ejecutar primero al agente principal
                # Convertimos los mensajes a textos que entiende el agente
                input_doctor = "\n".join(
                    f"{m['role'].upper()}: {m['content']}"
                    for m in st.session_state.messages
                    if m["role"] != "system"
                )
                salida_doctor = agente_doctor.run(input_doctor)

                #  Ahora pasamos la respuesta  al corrector
                # y le pedimos que la refine
                prompt_corrector = (
                    "Eres un Doctor altamente calificado, tu tarea es revisar el análisis preliminar del Doctor Banach:\n\n"
                    f"{salida_doctor}\n\n"
                    "Revísalo y corrige cualquier posible alucinación o error de interpretación, "
                    "manteniendo el mismo tono empático y claro."
                )
                salida_final = agente_corrector.run(prompt_corrector)

                response = salida_final

            except Exception as e:
                st.error(f"Error al comunicarse con Gemini: {e}")
                response = "Lo siento, hubo un error al procesar tu solicitud. Por favor, inténtalo de nuevo."


        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})