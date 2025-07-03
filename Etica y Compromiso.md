# Consideraciones Éticas y de Transparencia del Proyecto Banach

El desarrollo de herramientas de inteligencia artificial en el sector de la salud conlleva una profunda responsabilidad. El proyecto **Banach** ha sido concebido y construido sobre una base de principios éticos sólidos, diseñados para garantizar la seguridad del usuario, promover la comprensión y mantener una total transparencia sobre sus capacidades y limitaciones.

Este documento detalla nuestro marco ético, alineado con los principios fundamentales de la bioética y las mejores prácticas en el desarrollo de IA responsable.

## 1. Principios Bioéticos Fundamentales

Nuestro enfoque se guía por cuatro pilares de la ética médica, adaptados al contexto de una herramienta de asistencia por IA.

### **a. No Maleficencia (Primum non nocere): "Primero, no hacer daño"**

El principio más importante para Banach es la seguridad del usuario. Reconocemos que un diagnóstico o análisis incorrecto puede generar ansiedad y conducir a decisiones perjudiciales.

* **Asistente, no Sustituto:** Dejamos claro en toda la aplicación, especialmente durante la incorporación del usuario, que **Banach es una herramienta de apoyo educativo y de orientación, y no reemplaza el juicio clínico de un radiólogo certificado o un médico profesional**. La implementación de un `disclaimer` explícito, especialmente para el perfil "Paciente", es un mecanismo de seguridad fundamental [1].
* **Mitigación del Riesgo:** La función de la IA es ofrecer una primera interpretación estructurada y sugerir posibles vías de investigación, no proporcionar un diagnóstico definitivo. El lenguaje utilizado está cuidadosamente diseñado para evitar afirmaciones categóricas y fomentar la consulta con un experto humano.

### **b. Beneficencia: "Actuar en el mejor interés del usuario"**

Banach busca activamente generar un beneficio tangible para sus distintos tipos de usuarios.

* **Para Pacientes:** Reduce la brecha de conocimiento, traduciendo la complejidad de una imagen radiológica a un lenguaje comprensible y empático. Esto disminuye la incertidumbre y facilita conversaciones más informadas con sus médicos.
* **Para Estudiantes y Profesionales:** Sirve como una herramienta educativa interactiva, permitiendo correlacionar la teoría anatómica y patológica con casos visuales reales, y agilizando la identificación de hallazgos clave.
* **Arquitectura Adaptativa:** Nuestro sistema de doble agente es la clave para lograr la beneficencia. El primer agente ("El Doctor") asegura el rigor técnico, mientras que el segundo ("El Refinador") garantiza que la comunicación sea efectiva, clara y adecuada para el nivel de conocimiento del interlocutor.

### **c. Autonomía: "Respeto por la capacidad de decisión del individuo"**

Empoderamos a los usuarios dándoles información, pero siempre reforzando que la responsabilidad final de las decisiones clínicas recae en los profesionales de la salud.

* **Consentimiento Informado:** Al inicio de la interacción, el usuario no solo selecciona su perfil, sino que se le informa sobre el propósito y las limitaciones de la herramienta. Esto asegura que su participación sea informada y consciente.
* **Control del Usuario:** La interfaz permite al usuario controlar completamente la exploración de las imágenes (cortes, rotación), dándole un papel activo en el proceso de análisis.

### **d. Justicia y Equidad**

Buscamos que Banach sea una herramienta accesible y justa, aunque reconocemos los desafíos inherentes a los modelos de IA.

* **Accesibilidad:** Al ser una aplicación web desarrollada con Streamlit, eliminamos barreras de instalación de software complejo, haciéndola accesible desde cualquier dispositivo con un navegador.
* **Conciencia del Sesgo Algorítmico:** Somos conscientes de que los modelos de lenguaje masivos (LLM) como Gemini pueden contener sesgos inherentes derivados de sus datos de entrenamiento [2]. Nos comprometemos a:
    1.  Monitorear activamente las respuestas del modelo para detectar posibles sesgos.
    2.  Utilizar *prompts* de sistema que instruyan explícitamente al modelo para que proporcione análisis objetivos y evite generalizaciones.

## 2. Transparencia en el Funcionamiento

La confianza se construye sobre la transparencia. Es fundamental que los usuarios entiendan *cómo* funciona Banach.

### **a. Arquitectura de Agentes Inteligentes Explicada**

No ocultamos el proceso de la IA; lo presentamos como una de nuestras fortalezas.
1.  **Agente 1 - "El Doctor":** Este agente recibe la imagen y la consulta, realizando un primer análisis técnico y estructurado. Su salida es un "borrador" interno, enfocado en la precisión médica.
2.  **Agente 2 - "El Refinador":** Este agente toma el borrador técnico y lo traduce. Su única misión es refinar el lenguaje, asegurar la empatía y adaptar el tono al perfil del usuario (paciente, médico, etc.).
Este **enfoque de doble agente** es nuestra solución directa al desafío de ofrecer respuestas que sean a la vez técnicamente sólidas y humanamente comprensibles. El usuario final interactúa con el resultado del trabajo colaborativo de ambos agentes, obteniendo lo mejor de dos mundos: el rigor analítico y la comunicación efectiva.

### **b. Gestión de Datos y Privacidad**

La confidencialidad de los datos médicos es primordial.
* **Procesamiento Local:** Los archivos DICOM originales se procesan **localmente** en el entorno donde se ejecuta la aplicación. La carpeta que contiene los estudios médicos no se sube a la nube ni se comparte.
* **Interacción con la API:** Lo que se envía al modelo de IA (Google Gemini API) no es el archivo DICOM completo. Es una **representación visual en formato PNG** del corte específico que el usuario está viendo, codificada en base64. Junto a esta imagen temporal, se envía el historial de texto de la conversación para mantener el contexto.
* **Seguridad de Credenciales:** Las claves de API se gestionan de forma segura a través de variables de entorno (`.env`), evitando que queden expuestas en el código fuente.

## 3. Conclusión

El proyecto Banach es un ejercicio de innovación responsable. Entendemos que la IA en la salud es una frontera con un potencial inmenso, pero también con riesgos significativos. A través de un diseño centrado en el usuario, una arquitectura transparente de doble agente y un compromiso inquebrantable con los principios bioéticos, hemos creado una herramienta que busca ser segura, útil y fiable.

---

## Referencias

[1] World Health Organization. Ethics and governance of artificial intelligence for health: WHO guidance. Geneva: World Health Organization; 2021.

[2] Chen IY, Joshi I, Lew R, Ghassemi M. Caring for a new generation: Acknowledging and mitigating bias in medical AI. The Lancet Digital Health. 2024;6(4):e297-e300.

[3] Davenport T, Kalakota R. The potential for artificial intelligence in healthcare. Future Healthcare Journal. 2019;6(2):94-98.