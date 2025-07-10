import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Configura tu correo SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "jjusturi@gmail.com"
EMAIL_PASSWORD = "lccj glnd yfha kjhf"
EMAIL_RECEIVER = "jjusturi@gmail.com"

st.set_page_config(page_title="Registro de Evento", layout="centered")
st.title("🎉 Registro al Evento")
with st.expander("ℹ️ Instrucciones para rellenar el formulario"):
    st.markdown("""
    - Completa todos los campos obligatorios del formulario.
    - Proporciona información verídica y de contacto.
    - Si tienes necesidades especiales, indícalo en el campo correspondiente.
    - Al finalizar, pulsa **Enviar Registro** para completar tu inscripción.
    """)

with st.form("formulario_registro"):
    with st.expander("Información personal"):
        nombre = st.text_input("Nombre completo")
        correo = st.text_input("Correo electrónico")
        telefono = st.text_input("Teléfono de contacto")
        puesto = st.text_input("Puesto o cargo en la embarcación")
        empresa = st.text_input("Empresa o armador de la embarcación")

    with st.expander("Preguntas sobre el evento"):
        Uso_boyas = st.radio("¿Ha usado boyas satelitales alguna vez?", ["Sí", "No"])
        explicacion = st.text_area("Explique brevemente como las ha usado o qué le gustaría aprender sobre ellas",)
        necesidades = st.text_area("¿Tienes alguna necesidad especial del uso de boyas satelitales o comentario?")
        cambio = st.radio("¿Cambiarias el uso de tus boyas satelitales por las que has visto en este evento?", ["Sí", "No"])
    st.markdown(
        """
        <div style="font-size:0.95em; color:#888; margin-top:1em;">
        <b>Protección de datos:</b> Los datos proporcionados serán utilizados únicamente para la gestión del evento y no serán compartidos con terceros. Puedes solicitar la eliminación de tus datos en cualquier momento escribiendo a <a href="mailto:jjusturi@gmail.com">jjusturi@gmail.com</a>.
        </div>
        """,
        unsafe_allow_html=True
    )

    enviar = st.form_submit_button("Enviar Registro")

if enviar:
    # Validar que todos los campos estén completos
    campos_obligatorios = [
        nombre, correo, telefono, puesto, empresa,
        Uso_boyas, explicacion, necesidades, cambio
    ]
    if all(campos_obligatorios):
        # Componer el mensaje
        mensaje = f"""
        Nuevo registro al evento:

        Nombre: {nombre}
        Correo: {correo}
        Teléfono: {telefono}
        Puesto/Cargo: {puesto}
        Empresa/Armador: {empresa}
        ¿Ha usado boyas satelitales?: {Uso_boyas}
        Explicación: {explicacion}
        Necesidades/comentarios: {necesidades}
        ¿Cambiaría el uso de sus boyas?: {cambio}
        """

        # Enviar correo
        try:
            msg = MIMEText(mensaje)
            msg["Subject"] = "Nuevo Registro al Evento"
            msg["From"] = EMAIL_SENDER
            msg["To"] = EMAIL_RECEIVER

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            server.quit()

            st.success("🎉 ¡Registro enviado con éxito!")
        except Exception as e:
            st.error(f"❌ Error al enviar el correo: {e}")
    else:
        st.warning("⚠️ Por favor, completa todos los campos del formulario para enviar tu registro.")
