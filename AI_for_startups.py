import streamlit as st

# --- Configuración de la página ---
st.set_page_config(page_title="AI for Startups - Presentación", layout="centered")

# --- Slides de la presentación ---
slides = [
    {
        "title": "AI for Startups",
        "subtitle": "De la idea a la función: cómo usar la IA para escalar tu negocio 🚀",
        "content": "Basado en el ebook de CodeCodix",
        "image": "logo1.png"
    },
    {
        "title": "¿Qué es la IA realmente?",
        "content": """
        - IA = Enseñar a una máquina a hacer algo inteligente.
        - No es Skynet: es una herramienta, no un villano.
        - Ejemplos: reconocimiento facial, emails automáticos, recomendaciones.""",
        "image": "picture_imanol.png"
    },
    {
        "title": "¿Por qué usar IA en tu startup?",
        "content": """
        - Haces 15 trabajos al mismo tiempo.
        - La IA ahorra tiempo, dinero y esfuerzo.
        - No necesitas ser técnico para usarla.""",
        "image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?fit=crop&w=1000&q=80"
    },
    {
        "title": "Herramientas básicas para empezar",
        "content": """
        - ChatGPT: ideas, redacción.
        - Canva IA: diseño.
        - Zapier: automatiza tareas.
        - Grammarly: corrección automática.""",
        "image": "chatgpt_logo.png"
    },
    {
        "title": "IA para la Experiencia del Cliente",
        "content": """
        - Chatbots 24/7
        - Análisis de feedback
        - Recomendaciones personalizadas""",
        "image": "767.jpg"
    },
    {
        "title": "IA en Marketing y Ventas",
        "content": """
        - Segmentación inteligente
        - Creación de contenido (Jasper, Copy.ai)
        - CRM inteligente
        - Predicción de ventas""",
        "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?fit=crop&w=1000&q=80"
    },
    {
        "title": "IA en Operaciones y Producto",
        "content": """
        - Automatización de tareas
        - Optimización de inventario
        - A/B Testing
        - Desarrollo de prototipos
        """,
        "image": "imagen_producto.jpg"
    },
    {
        "title": "Casos de uso por industria",
        "content": """
        - Retail, Salud, Educación, Legal, Creatividad, Finanzas
        - ¡IA para todos los sectores!""",
        "image": "AI_industries.jpg"
    },
    {
        "title": "Cómo empezar con IA",
        "content": """
        - Detecta tu necesidad
        - Elige un proyecto piloto
        - Prueba herramientas (¡muchas son gratis!)
        - Escala poco a poco""",
        "image": "AI_man.jpg"
        
    },
    {
        "title": "El futuro es IA + humanos",
        "content": """
        - La IA no reemplaza, potencia.
        - Mantén el toque humano.
        - Escala con pocos recursos y mucha inteligencia.""",
        "image": "AI+humano.jpg"
    }
]

# --- Estado inicial ---
if "page" not in st.session_state:
    st.session_state.page = 0

# --- Mostrar slide actual ---
slide = slides[st.session_state.page]
st.image(slide["image"], width=300)
st.markdown(f"## {slide['title']}")
if "subtitle" in slide:
    st.markdown(f"#### {slide['subtitle']}")
st.markdown(slide["content"].replace("\\n", "\\n"))

# --- Navegación ---
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.session_state.page > 0:
        if st.button("⬅️ Anterior"):
            st.session_state.page -= 1
with col3:
    if st.session_state.page < len(slides) - 1:
        if st.button("Siguiente ➡️"):
            st.session_state.page += 1
