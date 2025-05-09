# BCSPromoter.py

import streamlit as st
from PIL import Image
import base64

# Configuración inicial
st.set_page_config(
    page_title="Conviértete en Promotor de BCS | CodeCodix",
    layout="centered",
    page_icon="💼"
)

# Imagen de fondo
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
            filter: blur(80px);
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("background1.jpg")

# Idioma
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

# Traducciones
texts = {
    "es": {
        "title": "💼 Sé parte del equipo :red[BCS Promoter]",
        "subtitle": "Gana dinero ayudando a empresas a digitalizarse con inteligencia artificial",
        "intro": """
        ¿Tienes una comunidad, contactos o redes sociales activas?  
        **Promociona BCS y gana el 50% de comisión por cada venta.**  
        ¡Con solo 4 clientes tu propia plataforma BCS será completamente **GRATIS**!
        """,
        "benefits_title": "🎯 ¿Por qué ser un Promotor de BCS?",
        "benefits": [
            "Comisión del **50%** por cada venta",
            "BCS gratis si traes 4 clientes",
            "No necesitas conocimientos técnicos",
            "Acceso a recursos y entrenamientos exclusivos",
            "Oportunidad de escalar como distribuidor oficial"
        ],
        "how_title": "🚀 ¿Cómo funciona?",
        "how": """
        1. **Solicita tu código de promotor personalizado**  
        2. Comparte nuestro contenido en tus redes o contactos  
        3. Cada venta hecha con tu código te da el **50% de comisión**  
        4. Si vendes a 4 clientes, ¡tu propia BCS será GRATIS!  
        """,
        "testimonies_title": "💬 Testimonios de Promotores",
        "testimonies": [
            "⭐️ *“Solo con compartir historias en Instagram logré vender 2 BCS. Nunca fue tan fácil monetizar mi red.”* – Laura (Emprendedora digital)",
            "⭐️ *“No soy experto en tecnología, pero la propuesta es tan clara que los clientes me buscan solos.”* – Andrés (Comerciante)"
        ],
        "cta_title": "✅ ¿Listo para comenzar?",
        "cta_msg": "**Solicita tu acceso como promotor hoy mismo.** ¡Es gratis y sin compromiso!",
        "cta_button": "💬 Solicitar Acceso por WhatsApp",
        "cta_whatsapp": "https://wa.me/5930993513082",
        "footer": "Desarrollado por CodeCodix | Transformando negocios con IA"
    },
    "en": {
        "title": "💼 Join the :red[BCS Promoter] Team",
        "subtitle": "Earn money helping businesses digitalize with AI",
        "intro": """
        Do you have a community, network or social presence?  
        **Promote BCS and earn 50% commission on each sale.**  
        Get your own BCS platform for **FREE** by referring just 4 clients!
        """,
        "benefits_title": "🎯 Why become a BCS Promoter?",
        "benefits": [
            "Earn **50%** commission per sale",
            "Get your BCS for free with 4 clients",
            "No technical knowledge needed",
            "Access to exclusive training and resources",
            "Opportunity to become an official distributor"
        ],
        "how_title": "🚀 How does it work?",
        "how": """
        1. **Request your custom promoter code**  
        2. Share BCS through your network or social media  
        3. Every sale with your code gives you **50% commission**  
        4. Get your own BCS for **FREE** after 4 clients!
        """,
        "testimonies_title": "💬 Promoter Testimonials",
        "testimonies": [
            "⭐️ *“Just by sharing stories on Instagram I sold 2 BCS. So easy!”* – Laura (Digital entrepreneur)",
            "⭐️ *“I’m not tech-savvy but clients come because it’s a clear value.”* – Andrés (Small business owner)"
        ],
        "cta_title": "✅ Ready to start?",
        "cta_msg": "**Request your access as a promoter now.** It's free and with no obligation!",
        "cta_button": "💬 Request via WhatsApp",
        "cta_whatsapp": "https://wa.me/5930993513082",
        "footer": "Developed by CodeCodix | Transforming businesses with AI"
    }
}

t = texts[lang]

# Contenido principal
st.image("logo1.png", width=200)
st.title(t["title"])
st.subheader(t["subtitle"])
st.markdown(t["intro"])

with st.expander(t["benefits_title"]):
    for b in t["benefits"]:
        st.markdown(f"- {b}")

with st.expander(t["how_title"]):
    st.markdown(t["how"])

with st.expander(t["testimonies_title"]):
    for test in t["testimonies"]:
        st.info(test)

# Call to action
st.markdown(f"## {t['cta_title']}")
st.success(t["cta_msg"])
if st.button(t["cta_button"]):
    st.markdown(f"[{t['cta_button']}]({t['cta_whatsapp']})", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption(t["footer"])
