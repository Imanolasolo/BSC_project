import streamlit as st

# Traducciones simples
content = {
    "es": {
        "title": "5 formas en que la IA ya está transformando industrias",
        "slides": [
            "Educación: plataformas que personalizan el aprendizaje.",
            "Salud: asistentes que clasifican pacientes y optimizan tiempos.",
            "Marketing: bots que generan contenido y lanzan campañas.",
            "Logística: algoritmos que predicen rutas y entregas.",
            "Legal: herramientas que resumen contratos automáticamente.",
        ],
        "cta": "¿Cómo podría aplicarse en tu industria?",
        "contact": "Hablemos por WhatsApp"
    },
    "en": {
        "title": "5 ways AI is already transforming industries",
        "slides": [
            "Education: platforms that personalize learning.",
            "Healthcare: assistants that classify patients and save time.",
            "Marketing: bots that generate content and launch campaigns.",
            "Logistics: algorithms that predict routes and deliveries.",
            "Legal: tools that summarize contracts automatically.",
        ],
        "cta": "How could this apply to your industry?",
        "contact": "Let's chat on WhatsApp"
    }
}

# Selector de idioma con botones de solo iconos
col1, col2 = st.columns([1, 10])
with col1:
    if st.button("🇺🇸", key="lang_en"):
        st.session_state.lang = "en"
with col2:
    if st.button("🇪🇸", key="lang_es"):
        st.session_state.lang = "es"

if "lang" not in st.session_state:
    st.session_state.lang = "es"  # Default language

data = content[st.session_state.lang]

st.title(data["title"])
st.markdown("###")

# Slide simple con botones
if "slide" not in st.session_state:
    st.session_state.slide = 0

col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("◀️"):
        st.session_state.slide = max(0, st.session_state.slide - 1)

with col2:
    st.info(data["slides"][st.session_state.slide])

with col3:
    if st.button("▶️"):
        st.session_state.slide = min(len(data["slides"]) - 1, st.session_state.slide + 1)

st.markdown("###")
st.success(data["cta"])

if st.button(data["contact"]):
    whatsapp_number = "5930993513082"
    message = "Hola Imanol! Vi tu carrusel sobre IA en industrias y me interesa crear algo juntos."
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message}"
    st.markdown(f"[{data['contact']}]({whatsapp_url})", unsafe_allow_html=True)
