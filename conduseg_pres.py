# landing_hospicor.py

import streamlit as st
from PIL import Image

st.set_page_config(page_title="BCS para Conduseg", layout="wide")
col1, col2 = st.columns([1, 4])
with col1:
# Banner o logo
    st.image("pablo_logo1.webp", width=200)

# Título principal
with col2:
    st.title(":red[BCS] para Conduseg")
    st.subheader("Automatiza, controla y escala tu operación con inteligencia artificial")


# Sección 1: Qué es un BCS
st.markdown("## ¿Qué es un BCS?")
st.write("""
Un **BCS (Business Core Software)** es una plataforma interactiva diseñada a la medida de tu empresa, que centraliza y automatiza tus procesos críticos. Más que un software, es el **corazón operativo digital** de tu organización.
""")

# Sección 2: ¿Qué puede hacer por Conduseg?
st.markdown("## ¿Cómo puede ayudar a Conduseg?")
st.success("""
- 🏥 Automatización del flujo de clientes y administración
- 🗃️ Gestión de historiales y documentos académicos con trazabilidad
- 🤖 Asistentes virtuales para consultas internas y externas
- 📊 Dashboard en tiempo real de indicadores clave
- 🧠 IA para análisis predictivo y soporte a la toma de decisiones
""")

if st.button("Chatea con BCS para conocer más"):
    chat_url = "https://bcs-customer-chat.streamlit.app/?embed_options=dark_theme" \
    ""
    st.markdown(f'<a href="{chat_url}" target="_blank">Ir al chat</a>', unsafe_allow_html=True)

# Sección 3: ¿Por qué elegir BCS?
st.markdown("## ¿Por qué elegir BCS?")
st.write("""
Un BCS es más que un software, es una solución integral que se adapta a tus necesidades específicas.""")
# Sección 4: Beneficios
st.markdown("## Beneficios para Conduseg")
cols = st.columns(3)
with cols[0]:
    st.metric("Reducción de errores", "⬇️ 70%")
    st.write("Evita duplicaciones y errores humanos en registros")
with cols[1]:
    st.metric("Ahorro de tiempo", "⏱️ +60%")
    st.write("Digitaliza tareas operativas y administrativas")
with cols[2]:
    st.metric("Visibilidad total", "📈 100%")
    st.write("Monitorea procesos desde cualquier dispositivo")

# Sección 5: CTA
st.markdown("## ¿Te gustaría transformar tu operación con BCS?")
lead = st.form("Contacto")
with lead:
    nombre = st.text_input("Tu nombre")
    email = st.text_input("Correo electrónico")
    cargo = st.text_input("Tu cargo")
    mensaje = st.text_area("¿Qué desafíos podríamos ayudarte a resolver?")
    submit = st.form_submit_button("Solicitar demo gratuita")

if submit:
    whatsapp_message = (
        f"Hola, soy {nombre} ({cargo}).\n"
        f"Correo: {email}\n"
        f"Mensaje: {mensaje}\n"
        "Solicito una demo gratuita de BCS para Conduseg."
    )
    whatsapp_link = f"https://wa.me/5930993513082?text={whatsapp_message.replace(' ', '%20').replace('\n', '%0A')}"
    st.success(f"Gracias, {nombre}! Haz clic en el siguiente enlace para enviar tu solicitud por WhatsApp.")
    st.markdown(f'<a href="{whatsapp_link}" target="_blank">Enviar por WhatsApp</a>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
🧠 Desarrollado por **Pablo Vidal Marketing** – Software inteligente para industrias visionarias.
""")
