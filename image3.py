import streamlit as st
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

def images3(uploaded_file):
    try:
        with open("temp_nii.nii.gz", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        img = nib.load("temp_nii.nii.gz")
        data = img.get_fdata()

        st.write("Dimensiones del volumen:", data.shape)

        if data.ndim < 4:
            st.warning("Los datos no son 4D. Mostrando el único volumen disponible.")
            vol = data 
        else:
            t = 0
            vol = data[:, :, :, t]

        fig, axes = plt.subplots(1, 3, figsize=(12, 4), dpi=200)
        fig.patch.set_facecolor('black')

        axes[0].imshow(vol[vol.shape[0]//2, :, :].T, cmap='gray', origin='lower')
        axes[0].set_title('Sagital', color='white')
        axes[0].axis('off')

        axes[1].imshow(vol[:, vol.shape[1]//2, :].T, cmap='gray', origin='lower')
        axes[1].set_title('Coronal', color='white')
        axes[1].axis('off')

        axes[2].imshow(vol[:, :, vol.shape[2]//2].T, cmap='gray', origin='lower')
        axes[2].set_title('Axial', color='white')
        axes[2].axis('off')

        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
        st.error("Por favor, asegúrate de que es un archivo NIfTI válido (.nii o .nii.gz).")