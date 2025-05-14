# landing_hospicor.py

import streamlit as st
from PIL import Image

st.set_page_config(page_title="BCS para Hospicor", layout="wide")

# Banner o logo
st.image("logo.svg", width=200)

# Título principal
st.markdown("""
# 🤖 BCS – Business Core Software para **Hospicor**
### Automatiza, controla y escala tu operación con inteligencia artificial
""")

# Sección 1: Qué es un BCS
st.markdown("## ¿Qué es un BCS?")
st.write("""
Un **BCS (Business Core Software)** es una plataforma interactiva diseñada a la medida de tu empresa, que centraliza y automatiza tus procesos críticos. Más que un software, es el **corazón operativo digital** de tu organización.
""")

# Sección 2: ¿Qué puede hacer por Hospicor?
st.markdown("## ¿Cómo puede ayudar a Hospicor?")
st.success("""
- 🏥 Automatización del flujo de pacientes y hospitalización
- 🗃️ Gestión de historiales y documentos clínicos con trazabilidad
- 🤖 Asistentes virtuales para atención interna y externa
- 📊 Dashboard en tiempo real de indicadores clave
- 🧠 IA para análisis predictivo y soporte a la toma de decisiones
""")

# Sección 3: ¿Por qué elegir BCS?
st.markdown("## ¿Por qué elegir BCS?")
st.write("""
Un BCS es más que un software, es una solución integral que se adapta a tus necesidades específicas.""")
# Sección 4: Beneficios
st.markdown("## Beneficios para Hospicor")
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
    st.success(f"Gracias, {nombre}! Te contactaremos pronto para coordinar la demo.")

# Footer
st.markdown("""
---
🧠 Desarrollado por **CodeCodix** – Software inteligente para industrias visionarias.
""")
