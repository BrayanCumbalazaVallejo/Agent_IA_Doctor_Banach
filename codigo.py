import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# Cargar el archivo NIfTI
img = nib.load('sub-0202_ses-01_task-rest_bold.nii.gz')

# Obtener los datos como un array de NumPy
data = img.get_fdata()  # Dimensiones: (X, Y, Z, T)

print("Dimensiones del volumen:", data.shape)

# Escoger un tiempo (por ejemplo, el primer volumen temporal)
t = 0
vol = data[:, :, :, t]  # Volumen en t=0

# Visualizar el corte medio en los tres ejes
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Eje sagital (X)
axes[0].imshow(vol[vol.shape[0]//2, :, :].T, cmap='gray', origin='lower')
axes[0].set_title('Sagital')

# Eje coronal (Y)
axes[1].imshow(vol[:, vol.shape[1]//2, :].T, cmap='gray', origin='lower')
axes[1].set_title('Coronal')

# Eje axial (Z)
axes[2].imshow(vol[:, :, vol.shape[2]//2].T, cmap='gray', origin='lower')
axes[2].set_title('Axial')

plt.tight_layout()
plt.show()