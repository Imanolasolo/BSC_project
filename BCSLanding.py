# bcs_landing.py

import streamlit as st
from PIL import Image
import base64

# Configuración inicial
st.set_page_config(
    page_title="BCS - Business Core Software | CodeCodix",
    layout="centered",
    page_icon="🤖"
)

# Set background image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def add_bg_from_local(bin_file):
    bg_image = get_base64_of_bin_file(bin_file)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{bg_image});
            background-size: cover;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: inherit;
            background-size: inherit;
            background-position: center;
            filter: blur(75px); /* Blur only the background */
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("background1.jpg")

# Translations
translations = {
    "es": {
        "title": "🚀 BCS – :red[Business Core Software]",
        "subtitle": "Transforma tu negocio con plataformas inteligentes diseñadas a tu medida",
        "welcome_title": "Bienvenidos a BCS",
        "welcome_content": """
        Bienvenido a **BCS**, la línea de plataformas interactivas con **Inteligencia Artificial** desarrolladas por **CodeCodix** para ayudarte a **automatizar, optimizar y escalar** tu negocio.  
        Ya seas emprendedor, empresa en crecimiento o institución educativa, nuestras soluciones te permiten integrar IA a tus procesos de forma sencilla y eficaz.
        """,
        "what_is_title": "¿Qué es BCS?",
        "what_is_content": """
        **BCS (Business Core Software)** no es una plataforma genérica, sino un conjunto de **soluciones personalizadas** diseñadas según tu industria y necesidad.  
        Cada BCS es creada desde cero para convertirse en el **núcleo digital operativo** de tu organización.

        ✔️ Chatbots especializados  
        ✔️ Automatización de tareas y procesos  
        ✔️ Gestión de ventas, agendas, atención y marketing  
        ✔️ Paneles de control y toma de decisiones inteligentes  
        ✔️ Totalmente adaptadas a tu marca, sector y flujo de trabajo
        """,
        "audience_title": "¿Para quién es?",
        "entrepreneurs": "👩‍💼 **Emprendedores**",
        "entrepreneurs_points": [
            "Escalabilidad inmediata",
            "Atención 24/7",
            "Ventas automáticas"
        ],
        "companies": "🏢 **Empresas**",
        "companies_points": [
            "Gestión interna optimizada",
            "Ahorro operativo",
            "Imagen innovadora"
        ],
        "education": "🎓 **Educación**",
        "education_points": [
            "Plataformas para universidades y escuelas",
            "Asistentes para estudiantes",
            "Procesos automatizados"
        ],
        "use_cases_title": "🌟 Casos de Uso",
        "use_cases": [
            "**Plataforma para Hospitales**: Automatización de admisión, seguimiento a pacientes, y asistentes virtuales médicos.",
            "**Plataforma para Escuelas**: Inscripción digital, chatbot para dudas estudiantiles y agenda automatizada.",
            "**Plataforma para Ecommerce**: Chatbot de ventas, gestión de pedidos, CRM y reportes inteligentes."
        ],
        "cta_title": "💬 ¿Quieres implementar BCS en tu negocio?",
        "cta_demo": "Agenda una demo gratuita o únete como colaborador para llevar BCS a tu comunidad o red.",
        "cta_contact": "👉 [Contáctanos vía WhatsApp](https://wa.me/5930993513082)",
        "cta_email": "📩 jjusturi@gmail.com",
        "footer": "Desarrollado por CodeCodix | Innovación con propósito",
        "copyright": "© 2024 CodeCodix. Todos los derechos reservados."
    },
    "en": {
        "title": "🚀 BCS – :red[Business Core Software]",
        "subtitle": "Transform your business with intelligent platforms tailored to your needs",
        "welcome_title": "Welcome to BCS",
        "welcome_content": """
        Welcome to **BCS**, the line of interactive platforms with **Artificial Intelligence** developed by **CodeCodix** to help you **automate, optimize, and scale** your business.  
        Whether you're an entrepreneur, a growing company, or an educational institution, our solutions allow you to integrate AI into your processes easily and effectively.
        """,
        "what_is_title": "What is BCS?",
        "what_is_content": """
        **BCS (Business Core Software)** is not a generic platform but a set of **customized solutions** designed according to your industry and needs.  
        Each BCS is created from scratch to become the **digital operational core** of your organization.

        ✔️ Specialized chatbots  
        ✔️ Task and process automation  
        ✔️ Sales, scheduling, customer service, and marketing management  
        ✔️ Dashboards and intelligent decision-making  
        ✔️ Fully adapted to your brand, sector, and workflow
        """,
        "audience_title": "Who is it for?",
        "entrepreneurs": "👩‍💼 **Entrepreneurs**",
        "entrepreneurs_points": [
            "Immediate scalability",
            "24/7 support",
            "Automated sales"
        ],
        "companies": "🏢 **Companies**",
        "companies_points": [
            "Optimized internal management",
            "Operational savings",
            "Innovative image"
        ],
        "education": "🎓 **Education**",
        "education_points": [
            "Platforms for universities and schools",
            "Assistants for students",
            "Automated processes"
        ],
        "use_cases_title": "🌟 Use Cases",
        "use_cases": [
            "**Platform for Hospitals**: Admission automation, patient tracking, and virtual medical assistants.",
            "**Platform for Schools**: Digital enrollment, chatbot for student inquiries, and automated scheduling.",
            "**Platform for Ecommerce**: Sales chatbot, order management, CRM, and intelligent reports."
        ],
        "cta_title": "💬 Want to implement BCS in your business?",
        "cta_demo": "Schedule a free demo or join as a collaborator to bring BCS to your community or network.",
        "cta_contact": "👉 [Contact us via WhatsApp](https://wa.me/5930993513082)",
        "cta_email": "📩 jjusturi@gmail.com",
        "footer": "Developed by CodeCodix | Innovation with purpose",
        "copyright": "© 2024 CodeCodix. All rights reserved."
    }
}

# Language selection
if "lang" not in st.session_state:
    st.session_state.lang = "es"

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🌐 Español"):
        st.session_state.lang = "es"
with col2:
    if st.button("🌐 English"):
        st.session_state.lang = "en"

lang = st.session_state.lang
t = translations[lang]

# Banner / Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo1.png", width=200)
with col2:
    st.title(t["title"])
st.subheader(t["subtitle"])

# Introducción
with st.expander(t["welcome_title"]):
    st.markdown(t["welcome_content"])

# Qué es BCS
with st.expander(t["what_is_title"]):
    st.markdown(t["what_is_content"])

# Beneficios por tipo de público
st.markdown(f"## {t['audience_title']}")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(t["entrepreneurs"])
    for point in t["entrepreneurs_points"]:
        st.markdown(f"- {point}")

with col2:
    st.markdown(t["companies"])
    for point in t["companies_points"]:
        st.markdown(f"- {point}")

with col3:
    st.markdown(t["education"])
    for point in t["education_points"]:
        st.markdown(f"- {point}")

# Testimonios / Casos de uso
st.markdown(f"## {t['use_cases_title']}")
for case in t["use_cases"]:
    st.info(case)

# Call to action
st.markdown(f"## {t['cta_title']}")
st.success(t["cta_demo"])
st.markdown(t["cta_contact"])
st.markdown(t["cta_email"])

# Promoter button
promoter_button_text = {
    "es": "¿Quieres hacer negocio siendo promotor de BCS?",
    "en": "Do you want to do business as a BCS promoter?"
}
promoter_url = "https://bcspromoter-landing.streamlit.app/?embed_options=dark_theme"
if st.button(promoter_button_text[lang]):
    st.markdown(f'<a href="{promoter_url}" target="_blank">{promoter_button_text[lang]}</a>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption(t["footer"])
st.markdown(t["copyright"])
