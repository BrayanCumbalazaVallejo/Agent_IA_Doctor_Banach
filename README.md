
![LOGO](https://cdn.discordapp.com/attachments/949495010829688942/1390158587913044119/logo.PNG?ex=68673d93&is=6865ec13&hm=0f922e7b16245234f1035f60701b631677daaa2fcdfe21adc1f5fe81b6a96cc1&)

# 👥 Integrantes

Brayan Armando Cumbalaza Vallejo

Santiago Abelardo Salcedo Rodriguez

Jerónimo Hoyos Botero

# 📝 Descripción del proyecto  Y El Problema Técnico

La interpretación de estudios de imagenología médica, como las tomografías computarizadas (TC), presenta dos desafíos técnicos fundamentales:

1.  **Manejo de Datos Volumétricos:** Los estudios médicos no son imágenes planas, sino series de archivos (generalmente en formato DICOM) que representan un volumen tridimensional. Su procesamiento requiere la lectura, ordenamiento y apilamiento de cientos de cortes para reconstruir el volumen anatómico, una tarea que debe ser eficiente y precisa.
2.  **Brecha de Comunicación y Contexto:** La información contenida en estas imágenes es densa y requiere conocimiento especializado. Un sistema de IA debe ser capaz no solo de "ver" la imagen, sino de interpretar la consulta del usuario en lenguaje natural y, lo más importante, **adaptar su respuesta al nivel de conocimiento del interlocutor** (paciente, estudiante de medicina o médico especialista). Una respuesta única para todos es ineficaz.

## Nuestra Solución: Arquitectura de Agentes Inteligentes Coordinados

Para resolver este problema, desarrollamos **Banach**, una aplicación web interactiva que implementa una arquitectura de agentes de IA coordinados para ofrecer un análisis preciso y adaptativo. El flujo técnico es el siguiente:

### 1. Procesamiento y Visualización del Volumen

* **Ingesta de Datos:** Utilizamos la biblioteca **Pydicom** en **Python** para el procesamiento de volúmenes de datos.
* **Visualizador Interactivo:** La interfaz, construida con **Streamlit**, permite al usuario navegar por este volumen. Se generan dinámicamente los tres planos anatómicos canónicos (Axial, Coronal y Sagital) mediante la transposición de los ejes del array de NumPy.

### 2. Sistema de Doble Agente con Gemini y LangChain

El núcleo de Banach es un sistema de dos agentes de IA que trabajan en secuencia: un **Agente Principal** y un **Agente Afinador**.

* **Agente N.º 1: "El Doctor" - Analista Especializado**
    * **Misión:** Realizar un primer análisis estructurado y técnico de la imagen.
    * **Funcionamiento:** Cuando el usuario envía una consulta, la imagen y el historial de la conversación se envían al modelo **Gemini** a través de **LangChain**.
    * **Inteligencia Adaptativa:** El prompt de sistema instruye al agente para que actúe como "Doctor Banach" y adapte su lenguaje según el perfil del usuario.

* **Agente N.º 2: "El Refinador" - Comunicador Empático**
    * **Misión:** Convertir el borrador técnico del primer agente en una respuesta final, pulida y clara.
    * **Funcionamiento:** La respuesta en borrador del Agente 1 **no se muestra al usuario**. En su lugar, se introduce en un segundo prompt que instruye a otro LLM para que "revise y refine" el análisis.
    * **Resultado:** Este segundo agente se encarga de suavizar el lenguaje y mejorar la empatía, asegurando la coherencia y presentando la información en primera persona como Doctor Banach.

Este enfoque de doble agente resuelve el problema de la comunicación contextual, permitiendo que Banach ofrezca análisis técnicamente sólidos con un nivel de claridad y empatía que un sistema de un solo paso difícilmente podría lograr.

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
# En la misma carpeta de app.py
echo "GOOGLE_API_KEY=tu_clave_gemini" >> .env
echo "DICOM_FOLDER_PATH=direccion_de_la_carpeta_de_dicoms" >> .env

#Activar streamlit
streamlit run desarrollo\app.py

#Para desactivar entorno
deactivate
```

# 📄 Licencia 
``` 
Este proyecto está distribuido bajo los términos de la licencia [MIT](https://opensource.org/licenses/MIT).  
Puedes usarlo, modificarlo y compartirlo libremente, siempre que conserves los avisos de copyright originales.
```
