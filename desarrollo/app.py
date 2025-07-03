# Herramientas
import numpy as np
import time
import os
import base64
import io
import pydicom
from dotenv import load_dotenv

# Visualización y parte gráfica
import matplotlib.pyplot as plt
import streamlit as st

# Manejo modelos de lenguaje
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# Funciones
def cargar_pixeldata_dicom(carpeta_dicoms: str):
    try:
        ordered_names = sorted(os.listdir(carpeta_dicoms))
        pixel_data = [pydicom.dcmread(os.path.join(carpeta_dicoms, name),force=True).pixel_array for name in ordered_names]
        return np.array(pixel_data, dtype="int16")
    except FileNotFoundError:
        st.error(f"Error: No se encontró el directorio de DICOMs en la ruta: '{carpeta_dicoms}'.")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error al cargar los archivos DICOM: {e}")
        return None

# Entornos de variable
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DICOM_FOLDER_PATH = os.getenv('DICOM_FOLDER_PATH')

# Modelos de Lenguaje
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=GOOGLE_API_KEY)
llm_2 = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1, google_api_key=GOOGLE_API_KEY)

st.set_page_config(layout="wide")

# Header interfaz
col1_header, col2_header = st.columns([1, 3])
with col1_header:
    # Logo
    st.image("assets\logo.PNG",  use_container_width=True)

with col2_header:
    # Descripción
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 1.5rem; border-radius: 10px; border: 1px solid #333; height: 100%;">
        <h3 style="color: #FFFFFF; margin-bottom: 0.8rem;">
            📝 <span style="color: #FF4B4B;">Descripción del</span> Proyecto
        </h3>
        <p style="color: #CCCCCC; font-size: 16px;">
            Esta herramienta combina la visualización médica con inteligencia artificial para brindar apoyo tanto a profesionales de la salud como a estudiantes y pacientes. 
            Permite explorar detalladamente <strong>cortes anatómicos</strong> de estudios médicos como tomografías o resonancias, mientras una IA especializada asiste en la comprensión y análisis de las imágenes.
        </p>
        <ul style="color: #AAAAAA; font-size: 15px; line-height: 1.7; padding-left: 20px;">
            <li style="margin-bottom: 10px;">
                🔬 <strong>Visualizador Interactivo:</strong> Explora cortes axiales, coronales y sagitales en tiempo real con controles intuitivos de deslizamiento, acercamiento y rotación en dispositivos móviles y de escritorio.
            </li>
            <li style="margin-bottom: 10px;">
                🤖 <strong>Análisis con IA:</strong> Recibe un primer análisis automatizado de la imagen médica, incluyendo hallazgos relevantes, sugerencias diagnósticas preliminares y preguntas de seguimiento.
            </li>
            <li style="margin-bottom: 10px;">
                🧠 <strong>Agentes Coordinados:</strong> Dos agentes de IA colaboran para brindar respuestas más precisas: uno especializado en lenguaje médico y otro en razonamiento visual.
            </li>
            <li style="margin-bottom: 10px;">
                🤝 <strong>Comunicación Adaptativa:</strong> El lenguaje se ajusta automáticamente si eres paciente, estudiante o personal clínico, facilitando una interacción clara y efectiva según tu nivel de conocimiento.
            </li>
            <li style="margin-bottom: 10px;">
                🌐 <strong>Aplicación Accesible:</strong> Funciona directamente desde el navegador, sin necesidad de instalación, lo que la hace ideal para consultas rápidas, educación médica y apoyo remoto.
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
st.divider()

# Cuerpo interfaz
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 1.2rem 1.5rem; border-radius: 10px; border: 1px solid #333; display: flex; align-items: center; gap: 0.8rem; min-height: 80px;">
        <div style='font-size: 30px;'>🧠</div>
        <h2 style='color: #FFFFFF; margin: 0;'><span style='color:#FF4B4B;'>Visualizador</span> de cortes</h2>
    </div>
    """, unsafe_allow_html=True)

    @st.cache_data
    def cargar_datos():
        return cargar_pixeldata_dicom(DICOM_FOLDER_PATH)
    
    volumen = cargar_datos()

    if volumen is not None:
        cortes_anatomicos = {"Axial": volumen, "Coronal": volumen.transpose(1, 0, 2), "Sagital": volumen.transpose(2, 0, 1)}
        corte = st.radio("Tipo Corte anatómico", ["Axial", "Coronal", "Sagital"], horizontal=True, key="corte_radio")
        vol = cortes_anatomicos[corte]
        index = st.slider(f"Corte {corte.lower()}", 0, vol.shape[0] - 1, vol.shape[0] // 2, key="corte_slider")
        grados_rotacion = st.slider("Rotar imagen (grados)", 0, 270, 0, 90, key="rotacion_slider")
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

# Chat con el agente de IA
with col2:
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 1.2rem 1.5rem; border-radius: 10px; border: 1px solid #333; display: flex; align-items: center; gap: 0.8rem; min-height: 80px;">
        <div style='font-size: 30px;'>💬</div>
        <h2 style='color: #FFFFFF; margin: 0;'><span style='color:#FF4B4B;'>Asistencia</span> de Banach</h2>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [] 
        st.session_state.display_messages = []
        st.session_state.user_role = None
        
        welcome_msg1 = {"role": "assistant", "content": "¡Hola! Soy el Dr. Banach, tu asistente de radiología."}
        welcome_msg2 = {"role": "assistant", "content": "Para personalizar mi análisis, por favor, **selecciona tu rol**:"}
        st.session_state.messages.extend([welcome_msg1, welcome_msg2])
        st.session_state.display_messages.extend([welcome_msg1, welcome_msg2])

    for msg in st.session_state.display_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if not st.session_state.user_role:
        col_paciente, col_medico, col_afin = st.columns(3)

        with col_paciente:
            # Elegir perfil del usuario
            if st.button("Soy Paciente", use_container_width=True):
                st.session_state.user_role = "paciente"
                
                disclaimer_msg = {"role": "assistant", "content": "Gracias. Usaré un lenguaje sencillo y claro. **Es muy importante recordar que soy un asistente virtual. Mis análisis son una orientación y no reemplazan el diagnóstico de un médico certificado. Cualquier decisión sobre tu salud debe ser consultada y supervisada por un profesional.**"}
                follow_up_msg = {"role": "assistant", "content": "Dicho esto, ¿te ayudo a interpretar los datos de la imagen?"}
                
                st.session_state.messages.extend([disclaimer_msg, follow_up_msg])
                st.session_state.display_messages.extend([disclaimer_msg, follow_up_msg])
                st.rerun()

        with col_medico:
            if st.button("Soy Médico/Estudiante", use_container_width=True):
                st.session_state.user_role = "médico"
                confirmation_msg = {"role": "assistant", "content": "Entendido. Adaptaré mis explicaciones con terminología técnica. Escribe tu consulta."}
                st.session_state.messages.append(confirmation_msg)
                st.session_state.display_messages.append(confirmation_msg)
                st.rerun()

        with col_afin:
            if st.button("Afín a la salud", use_container_width=True):
                st.session_state.user_role = "afín"
                confirmation_msg = {"role": "assistant", "content": "Perfecto. Me enfocaré en hallazgos prácticos. ¿En qué puedo ayudarte?"}
                st.session_state.messages.append(confirmation_msg)
                st.session_state.display_messages.append(confirmation_msg)
                st.rerun()

    else:
        if prompt := st.chat_input("Escribe tu mensaje sobre la imagen..."):
            user_msg = {"role": "user", "content": prompt}
            st.session_state.messages.append(user_msg)
            st.session_state.display_messages = [user_msg]
            st.rerun()
            
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            #Agente 1 Doctor Banach
        with st.spinner("El Dr. Banach está analizando la imagen..."):
            try:
                role_instruction = {
                    "paciente": "si es un paciente, usa lenguaje muy sencillo, sin tecnicismos y con analogías.",
                    "médico": "si es medico o estudiante de medicina, puedes usar lenguaje medico, pero explica terminos complejos si es necesario.",
                    "afín": "si es personal afín a la salud, enfócate en los hallazgos prácticos y los pasos a seguir."
                }
                system_prompt = f"""
                    Eres el Doctor Banach, un asistente médico virtual especializado en radiología. Tu misión es analizar la imagen proporcionada.
                    Sigue esta estructura:
                    1. Orientación: Describe la vista (axial, coronal, sagital).
                    2. Hallazgos principales: Describe brevemente lo que ves y su ubicación.
                    3. Diagnósticos diferenciales: Ofrece hasta 2 posibles causas.
                    4. Siguiente paso sugerido: Recomienda un examen o consulta.
                    5. Interacción: Termina con "Si quieres que comparemos con otro corte, indícalo."
                    6. Tono: Sé tranquilizador, empático y recuerda que no reemplazas a un radiólogo humano.
                    Condición de lenguaje: {role_instruction.get(st.session_state.user_role, 'paciente')}
                    No reveles que eres una IA.
                """

                #  historial de la conversación 
                history_messages = []
                for msg in st.session_state.messages[:-1]:
                    if msg['role'] == 'user':
                        history_messages.append(HumanMessage(content=msg['content']))
                    elif msg['role'] == 'assistant':
                        history_messages.append(AIMessage(content=msg['content']))

                # 2. mensaje final del usuario
                last_user_prompt_text = st.session_state.messages[-1]['content']
                final_user_message_content = [
                    {"type": "text", "text": last_user_prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{st.session_state.current_dicom_image_base64}"}
                    }
                ]

                # formato correcto para el modelo
                messages_for_llm = [
                    HumanMessage(content=system_prompt),
                    *history_messages,
                    HumanMessage(content=final_user_message_content)
                ]

                salida_doctor_borrador = llm.invoke(messages_for_llm)

                #Agente 2 refinación
                prompt_refinador = f"""
                    Eres el Doctor Banach. Has realizado un análisis preliminar de una imagen médica.
                    Este es tu borrador de pensamientos:
                    ---
                    {salida_doctor_borrador.content}
                    ---
                    Ahora, refina este borrador para presentarlo como tu análisis final y definitivo al usuario.
                    Habla siempre en primera persona, como Doctor Banach. No menciones que esto es un borrador o una revisión.
                    Asegúrate de que la respuesta sea precisa, clara, siga la estructura solicitada y mantenga un tono empático y profesional.
                """
                salida_final_msg = llm_2.invoke(prompt_refinador)
                response = salida_final_msg.content

            except Exception as e:
                st.error(f"Error al comunicarse con Gemini: {e}")
                response = "Lo siento, hubo un error al procesar tu solicitud. Por favor, inténtalo de nuevo."

            assistant_msg = {"role": "assistant", "content": response}
            st.session_state.messages.append(assistant_msg)
            st.session_state.display_messages.append(assistant_msg)
            st.rerun()