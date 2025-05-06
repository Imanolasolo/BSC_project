import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import base64
import os  

# Set page config
st.set_page_config(page_title="BCS AI", page_icon="🧠", layout="wide")

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
        "title": "🧠 BCS AI: Tu Plataforma Empresarial Inteligente",
        "subtitle": "Automatiza, gestiona y evoluciona con nuestra solución todo-en-uno",
        "intro": "Bienvenido a **BCS AI** (Business Core Solution), una plataforma diseñada para transformar digitalmente tu negocio con inteligencia artificial.",
        "cta_register": "¡Regístrate ahora y transforma tu negocio!",
        "cta_register_content": "Regístrate para acceder a todas las funcionalidades de nuestra plataforma y transformar tu negocio con inteligencia artificial.",
        "cta_register_why": "**¿Por qué registrarte?**",
        "cta_register_points": [
            "Obtén acceso exclusivo a herramientas avanzadas de gestión empresarial.",
            "Descubre cómo la inteligencia artificial puede optimizar tus procesos.",
            "Únete a una comunidad de empresas innovadoras que ya están marcando la diferencia."
        ],
        "cta_collaborate": "Colabora con nosotros y sé parte del cambio",
        "cta_collaborate_content": "Colabora con nosotros para ser parte de un ecosistema innovador que está cambiando la forma de hacer negocios.",
        "cta_collaborate_why": "**¿Por qué colaborar?**",
        "cta_collaborate_points": [
            "Participa en proyectos de vanguardia que están transformando industrias.",
            "Comparte tus ideas y contribuye al desarrollo de soluciones tecnológicas.",
            "Amplía tu red de contactos y oportunidades de negocio."
        ],
        "cta_invest": "Invierte en el futuro de la tecnología empresarial",
        "cta_invest_content": "Invierte en el futuro de la tecnología empresarial y sé parte del crecimiento de BCS AI.",
        "cta_invest_why": "**¿Por qué invertir?**",
        "cta_invest_points": [
            "Sé parte de una empresa con un modelo de negocio sólido y en crecimiento.",
            "Aprovecha el auge de la inteligencia artificial en el mercado empresarial.",
            "Obtén retornos significativos mientras apoyas la innovación tecnológica."
        ],
        "testimonials_title": "💬 Testimonios",
        "testimonials": [
            "BCS AI ha revolucionado la forma en que gestionamos nuestros clientes. - Empresa X",
            "Gracias a BCS AI, hemos ahorrado tiempo y recursos. - Usuario Y"
        ],
        "benefits_title": "🚀 Beneficios de BCS AI",
        "benefits": [
            "Automatización de procesos",
            "Gestión avanzada de clientes",
            "Herramientas de comunicación integradas",
            "Soporte personalizado"
        ],
        "register_form_title": "📋 Regístrate ahora",
        "name": "Nombre",
        "email": "Correo electrónico",
        "register": "Registrarse",
        "roles_title": "🌟 Roles en BCS AI",
        "roles": {
            "admin": "👑 **Admin**: Gestiona usuarios y supervisa la plataforma.",
            "guest": "👤 **Guest**: Explora la plataforma en modo demo.",
            "starter": "🚀 **Starter**: Maneja tus clientes con un CRM básico.",
            "company": "🏢 **Company**: Gestiona clientes con un CRM avanzado y herramientas de comunicación.",
            "promoter": "📢 **Promoter**: Promociona la app y gestiona referencias."
        },
        "contact_title": "📲 Contáctanos",
        "message": "¿Cómo podemos ayudarte?",
        "send": "Enviar mensaje por WhatsApp",
        "whatsapp_note": "Nuestro equipo te atenderá personalmente por WhatsApp. ¡Trato directo y sin intermediarios!"
    },
    "en": {
        "title": "🧠 BCS AI: Your Intelligent Business Platform",
        "subtitle": "Automate, manage, and grow with our all-in-one solution",
        "intro": "Welcome to **BCS AI** (Business Core Solution), a platform designed to digitally transform your business with artificial intelligence.",
        "cta_register": "Sign up now and transform your business!",
        "cta_register_content": "Register to access all the features of our platform and transform your business with artificial intelligence.",
        "cta_register_why": "**Why register?**",
        "cta_register_points": [
            "Gain exclusive access to advanced business management tools.",
            "Discover how artificial intelligence can optimize your processes.",
            "Join a community of innovative companies already making a difference."
        ],
        "cta_collaborate": "Collaborate with us and be part of the change",
        "cta_collaborate_content": "Collaborate with us to be part of an innovative ecosystem that is changing the way business is done.",
        "cta_collaborate_why": "**Why collaborate?**",
        "cta_collaborate_points": [
            "Participate in cutting-edge projects that are transforming industries.",
            "Share your ideas and contribute to the development of technological solutions.",
            "Expand your network of contacts and business opportunities."
        ],
        "cta_invest": "Invest in the future of business technology",
        "cta_invest_content": "Invest in the future of business technology and be part of BCS AI's growth.",
        "cta_invest_why": "**Why invest?**",
        "cta_invest_points": [
            "Be part of a company with a solid and growing business model.",
            "Take advantage of the rise of artificial intelligence in the business market.",
            "Achieve significant returns while supporting technological innovation."
        ],
        "testimonials_title": "💬 Testimonials",
        "testimonials": [
            "BCS AI has revolutionized how we manage our clients. - Company X",
            "Thanks to BCS AI, we have saved time and resources. - User Y"
        ],
        "benefits_title": "🚀 Benefits of BCS AI",
        "benefits": [
            "Process automation",
            "Advanced client management",
            "Integrated communication tools",
            "Personalized support"
        ],
        "register_form_title": "📋 Sign Up Now",
        "name": "Name",
        "email": "Email",
        "register": "Register",
        "roles_title": "🌟 Roles in BCS AI",
        "roles": {
            "admin": "👑 **Admin**: Manage users and oversee the platform.",
            "guest": "👤 **Guest**: Explore the platform in demo mode.",
            "starter": "🚀 **Starter**: Manage your clients with a basic CRM.",
            "company": "🏢 **Company**: Manage clients with advanced CRM and communication tools.",
            "promoter": "📢 **Promoter**: Promote the app and manage referrals."
        },
        "contact_title": "📲 Contact Us",
        "message": "How can we help you?",
        "send": "Send WhatsApp Message",
        "whatsapp_note": "Our team will assist you personally on WhatsApp. Direct and personal contact!"
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

# Content
st.title(t["title"])
st.subheader(t["subtitle"])
st.markdown(t["intro"])

# Call-to-Actions
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    
    with st.expander(t['cta_register']):
        st.write(t['cta_register_content'])
        st.write(t['cta_register_why'])
        for point in t['cta_register_points']:
            st.write(f"- {point}")
with col2:
    
    with st.expander(t['cta_collaborate']):
        st.write(t['cta_collaborate_content'])
        st.write(t['cta_collaborate_why'])
        for point in t['cta_collaborate_points']:
            st.write(f"- {point}")

with col3:
    
    with st.expander(t['cta_invest']):
        st.write(t['cta_invest_content'])
        st.write(t['cta_invest_why'])
        for point in t['cta_invest_points']:
            st.write(f"- {point}")

# Benefits Section
st.markdown("---")
st.markdown(f"### {t['benefits_title']}")
for benefit in t['benefits']:
    st.markdown(f"- {benefit}")

# Roles Section
st.markdown("---")
st.markdown(f"### {t['roles_title']}")
for role, description in t["roles"].items():
    st.markdown(description)

# Registration Form
st.markdown("---")
st.subheader(t["register_form_title"])
name = st.text_input(t["name"])
email = st.text_input(t["email"])
if st.button(t["register"]):
    base_url = "https://wa.me/5930993513082"
    full_message = f"Hola! Soy {name}, mi correo es {email}. Quiero registrarme en BCS." if lang == "es" else f"Hello! I am {name}, my email is {email}. I want to register in BCS."
    url = f"{base_url}?text={urllib.parse.quote(full_message)}"
    st.markdown(f"[👉 {t['send']}]({url})", unsafe_allow_html=True)

# Contact Section
st.markdown("---")
st.subheader(t["contact_title"])
message = st.text_area(t["message"])

if st.button(t["send"]):
    base_url = "https://wa.me/5930993513082"
    full_message = f"Hola! Soy {name}, mi correo es {email}. {message}" if lang == "es" else f"Hello! I am {name}, my email is {email}. {message}"
    url = f"{base_url}?text={urllib.parse.quote(full_message)}"
    st.markdown(f"[👉 {t['send']}]({url})", unsafe_allow_html=True)

st.caption(t["whatsapp_note"])
