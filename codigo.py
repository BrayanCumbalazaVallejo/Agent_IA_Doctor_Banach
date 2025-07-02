import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

col_tomografia, col_chat = st.columns([0.6, 0.4], gap="large")

with col_tomografia:
    st.header("Visor de Resonancia")

    placeholder_img = np.zeros((512, 512), dtype=np.uint8)
    st.image(
        placeholder_img,
        caption="Sube un archivo .nii.gz para comenzar el análisis",
        use_column_width=True
    )
    
    slice_index = st.slider(
        "Seleccionar corte (slice)",
        min_value=0,
        max_value=155, 
        value=78,
        help="Mueve el dial para navegar por los diferentes cortes de la imagen."
    )

with col_chat:
    st.header("NeuroScan AI")

    report_container = st.container(height=450, border=True)
    
    report_container.markdown("""
    **Informe de Pre-análisis:**
    
    - **ID de Imagen:** sub-01_run-01_T2w
    - **Modalidad:** T2-weighted MRI
    
    **Hallazgos Descriptivos:**
    1.  **Ventrículos Laterales:** Morfología y tamaño dentro de los límites de la normalidad para el grupo de edad de referencia. No se observa hidrocefalia.
    2.  **Sustancia Gris-Blanca:** Diferenciación conservada. No se identifican lesiones focales evidentes, edema o áreas de restricción a la difusión en las secuencias evaluadas.
    3.  **Fosa Posterior:** Cerebelo y tronco encefálico sin alteraciones significativas.
    
    ---
    
    *`Advertencia: Este es un análisis preliminar generado por una IA y no constituye un diagnóstico médico. La interpretación final debe ser realizada por un radiólogo certificado.`*
    """)

    prompt = st.chat_input("Describe qué analizar en la imagen...")

    if prompt:
        report_container.info(f"Pregunta del usuario: {prompt}")