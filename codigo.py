import streamlit as st
import numpy as np
import pydicom
import os
import zipfile
import tempfile

st.set_page_config(layout="wide")

def cargar_pixeldata_dicom(carpeta_dicoms: str):
    ordered_names = sorted(os.listdir(carpeta_dicoms))
    pixel_data = []
    for name in ordered_names:
        try:
            dcm_path = os.path.join(carpeta_dicoms, name)
            if os.path.isfile(dcm_path):
                pixel_data.append(pydicom.dcmread(dcm_path).pixel_array)
        except pydicom.errors.InvalidDicomError:
            continue
    return np.array(pixel_data, dtype="int16")

col_tomografia, col_chat = st.columns([0.6, 0.4], gap="large")

with col_tomografia:
    st.header("Visor de Resonancia DICOM")

    uploaded_file = st.file_uploader(
        "Sube un archivo .zip con la serie de DICOMs",
        type=['zip']
    )

    if uploaded_file is not None:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, uploaded_file.name)
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                image_data = cargar_pixeldata_dicom(temp_dir)

                if image_data.ndim == 3 and image_data.shape[0] > 1:
                    num_slices = image_data.shape[0]
                    default_slice = num_slices // 2

                    slice_index = st.slider(
                        "Seleccionar corte (slice)",
                        min_value=0,
                        max_value=num_slices - 1,
                        value=default_slice,
                        help="Mueve el dial para navegar por los diferentes cortes de la imagen."
                    )

                    slice_to_show = image_data[slice_index, :, :]

                    st.image(
                        slice_to_show,
                        caption=f"Mostrando corte {slice_index + 1} de {num_slices}",
                        use_column_width=True,
                        clamp=True
                    )
                else:
                    st.error("El archivo .zip no contiene una serie de imágenes DICOM válida.")

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

    else:
        placeholder_img = np.zeros((512, 512), dtype=np.uint8)
        st.image(
            placeholder_img,
            caption="Sube un archivo .zip para comenzar el análisis",
            use_column_width=True
        )
        st.slider(
            "Seleccionar corte (slice)",
            min_value=0,
            max_value=0,
            value=0,
            disabled=True
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