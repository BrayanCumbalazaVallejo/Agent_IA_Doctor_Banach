import numpy as np

#Visualización
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Acceder a los Dicom
import os
import pydicom


def cargar_pixeldata_dicom(carpeta_dicoms: str):
    """
    Genera un np array valores de gris de 3 dimensiones de la forma (axial,sagital,coronal) a partir de un directorio de dicoms
    """
    ordered_names = sorted(os.listdir(carpeta_dicoms))
    pixel_data = [pydicom.dcmread(os.path.join(carpeta_dicoms, name)).pixel_array for name in ordered_names] 
    return np.array(pixel_data,dtype="int16")