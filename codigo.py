import streamlit as st
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# --- Inicialización del estado de la sesión ---
if 'nii_data' not in st.session_state:
    st.session_state.nii_data = None
if 'nii_filename' not in st.session_state:
    st.session_state.nii_filename = ""

# --- Definición de Columnas ---
col_tomografia, col_chat = st.columns([0.6, 0.4], gap="large")


# --- Columna Izquierda: Visualizador ---
with col_tomografia:
    st.header("Visor de Resonancia")

    uploaded_file = st.file_uploader(
        "Sube un archivo .nii o .nii.gz",
        type=['nii', 'nii.gz']
    )

    # Si se sube un nuevo archivo, se carga en el estado de la sesión
    if uploaded_file is not None:
        try:
            img = nib.load(uploaded_file.name, mmap=False) 
            st.session_state.nii_data = img.get_fdata()
            st.session_state.nii_filename = uploaded_file.name
            st.success(f"¡Archivo '{uploaded_file.name}' cargado!")
        except Exception as e:
            st.error(f"Error al leer el archivo NIfTI: {e}")
            st.session_state.nii_data = None


    # El contenedor de la imagen se actualiza dinámicamente
    image_container = st.empty()

    if st.session_state.nii_data is not None:
        data = st.session_state.nii_data
        
        # Determina el eje de visualización y el número máximo de cortes
        axis_options = ["Axial", "Sagital", "Coronal"]
        selected_axis = st.selectbox("Seleccionar plano de visualización", axis_options)

        axis_map = {"Axial": 2, "Sagital": 0, "Coronal": 1}
        axis_idx = axis_map[selected_axis]
        
        max_slices = data.shape[axis_idx] - 1
        
        slice_index = st.slider(
            f"Seleccionar corte ({selected_axis})",
            min_value=0,
            max_value=max_slices,
            value=max_slices // 2,
            help="Mueve el dial para navegar por los diferentes cortes de la imagen."
        )

        # Selecciona el corte correcto según el eje
        if selected_axis == "Axial":
            slice_to_show = data[:, :, slice_index].T
        elif selected_axis == "Sagital":
            slice_to_show = data[slice_index, :, :].T
        else: # Coronal
            slice_to_show = data[:, slice_index, :].T

        image_container.image(
            slice_to_show,
            caption=f"Mostrando corte {slice_index} del archivo {st.session_state.nii_filename}",
            use_column_width=True,
            clamp=True
        )

    else:
        # Muestra la imagen de placeholder si no hay datos cargados
        placeholder_img = np.zeros((512, 512), dtype=np.uint8)
        image_container.image(
            placeholder_img,
            caption="Sube un archivo .nii.gz para comenzar el análisis",
            use_column_width=True
        )


# --- Columna Derecha: Chat (se mantiene igual que tu código) ---
with col_chat:
    st.header("NeuroScan AI")

    report_container = st.container(height=450, border=True)
    
    # Este contenido puede ser dinámico en el futuro
    report_container.markdown("""
    **Informe de Pre-análisis:**
    
    - **ID de Imagen:** `(Esperando archivo)`
    - **Modalidad:** `(N/A)`
    
    **Hallazgos Descriptivos:**
    1.  **Ventrículos Laterales:** Esperando datos...
    2.  **Sustancia Gris-Blanca:** Esperando datos...
    3.  **Fosa Posterior:** Esperando datos...
    
    ---
    
    *`Advertencia: Este es un análisis preliminar generado por una IA y no constituye un diagnóstico médico. La interpretación final debe ser realizada por un radiólogo certificado.`*
    """)

    prompt = st.chat_input("Describe qué analizar en la imagen...")

    if prompt:
        report_container.info(f"Pregunta del usuario: {prompt}")