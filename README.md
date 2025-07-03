
![LOGO](https://cdn.discordapp.com/attachments/949495010829688942/1390158587913044119/logo.PNG?ex=68673d93&is=6865ec13&hm=0f922e7b16245234f1035f60701b631677daaa2fcdfe21adc1f5fe81b6a96cc1&)

# 👥 Integrantes

Brayan Cumbalaza

Santiago Salcedo

Jerónimo Hoyos Botero

# 📝 Descripción del proyecto
Esta herramienta interactiva permite visualizar cortes anatómicos (axial, coronal y sagital) a partir de estudios médicos (como TAC o resonancias), y proporciona asistencia para la interpretación inicial de las imágenes.

El objetivo es facilitar tanto el análisis técnico como el entendimiento por parte del paciente o especialista.

🔄 Visualización en tiempo real

🔃 Rotación e inspección por cortes

🧭 Soporte de diferentes vistas anatómicas 

---

# 🛠 Stack Tecnológico 

### 🖥️ Backend y procesamiento
- **Python** como lenguaje principal.
- Librerías clave para procesamiento de imágenes médicas:
  - `pydicom`: carga archivos DICOM.
  - `numpy`: manejo de matrices 3D.
  - `matplotlib`: visualización de imágenes.
- Soporte para visualización de cortes:
  - **Axial**, **Sagital**, **Coronal**.
  - Incluye control de rotación de imágenes.

### 🧠 Inteligencia Artificial
- **Google Gemini API**, integrado con `langchain`.
- El modelo:
  - Recibe imágenes médicas en formato PNG (base64).
  - Responde con explicaciones simples, empáticas y en lenguaje natural.
- Clave API segura usando `.env`.

### 🖼️ Interfaz de usuario (UI)
- Hecha con **Streamlit**:
  - Visualización interactiva de cortes médicos.
  - Sliders para navegar y rotar los cortes.
  - **Chat médico** simulado que usa IA para interpretar y explicar las imágenes.
- Estética personalizada con HTML + colores oscuros.

### 🔐 Seguridad
- Uso de `python-dotenv` para proteger la clave de API.
- El estado de sesión guarda historial del chat y la imagen actual.

---

# 🚀 Instalación y Configuración  

### **Requisitos**  
- Python 3.10+  
- Claves de API para Google Gemini (almacenadas en variables de entorno).  
- Carpeta archivos médicos en formato DICOM
### **Pasos para la instalación**  
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/Hackaton_DeepPunk_Doc_Banach

# Entrar al directorio del Desarrollo
cd Agent_IA_Doctor_Banach/desarrollo

# Crear entorno virtual (Python)
python -m venv .venv
source venv/bin/activate  # Linux/Mac
.venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (crear archivo .env)
echo "GOOGLE_API_KEY=tu_clave_gemini" >> .env
echo "DICOM_FOLDER_PATH=direccion_de_la_carpeta_de_dicoms" >> .env

#Activar streamlit
streamlit run app.py

#Para desactivar entorno
deactivate
```

# 📄 Licencia 
``` 
Este proyecto está distribuido bajo los términos de la licencia [MIT](https://opensource.org/licenses/MIT).  
Puedes usarlo, modificarlo y compartirlo libremente, siempre que conserves los avisos de copyright originales.
```
