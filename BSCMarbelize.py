import streamlit as st

import base64

# Configuración inicial
st.set_page_config(
    page_title="BCS - Marbelize | CodeCodix",
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

# Encabezado principal
st.title("Potencia la eficiencia operativa de Marbelize S.A.")
st.subheader("Business Core Software (BCS) personalizado para la industria atunera")

# Imagen de fondo o logo (opcional)
st.image("marbelize_logo.jpeg", width=200)

# Sección: ¿Qué es un BCS?
st.markdown("### ¿Qué es un BCS?")
st.markdown("""
Un **Business Core Software (BCS)** es una solución tecnológica hecha a medida para digitalizar, automatizar y optimizar procesos internos y externos de una empresa.  
Incluye módulos interactivos como:

- **Asistentes Virtuales Inteligentes**
- **Plataformas CRM y ERP**
- **Landing pages dinámicas para campañas B2B/B2C**
- **Control y monitoreo de producción**
- **Herramientas de trazabilidad y logística**
- **Tableros interactivos y reportes en tiempo real**
""")
if st.button("Chatea con BCS para conocer más"):
    chat_url = "https://bcs-customer-chat.streamlit.app/"
    st.markdown(f'<a href="{chat_url}" target="_blank">Ir al chat</a>', unsafe_allow_html=True)


# Sección: ¿Por qué Marbelize?
st.markdown("### ¿Por qué Marbelize?")
st.markdown("""
Marbelize cuenta con una operación de alto nivel en procesamiento de atún, control de calidad y trazabilidad. Un BCS puede integrar:

- Registro y control de lotes desde pesca hasta empaque
- CRM interno para el equipo de ventas/exportación
- Automatización de auditorías internas y externas (BRC, IFS, Kosher)
- Paneles para trazabilidad, logística y producción en tiempo real
- Soporte de inteligencia artificial para análisis predictivo y gestión de planta
""")

# Sección: Beneficios claves
st.markdown("### Beneficios inmediatos")
st.success("Incremento de eficiencia operativa hasta un 40%")
st.success("Reducción de errores humanos y tiempos muertos")
st.success("Mejora en el control de calidad y cumplimiento")
st.success("Decisiones basadas en datos en tiempo real")

# Sección: CTA
st.markdown("## ¿Quieres conocer cómo funcionaría en Marbelize?")
st.markdown("Agenda una demostración personalizada o solicita un diagnóstico gratuito.")

# Botón para agendar reunión
if st.button("Solicitar una demo gratuita"):
    whatsapp_message = "Marbelize solicita una demo gratuita y una reunion para ver los alcances de BCS"
    whatsapp_number = "+5930993513082"
    whatsapp_link = f"https://wa.me/{whatsapp_number}?text={whatsapp_message.replace(' ', '%20')}"
    st.markdown(f'<a href="{whatsapp_link}" target="_blank">Haz clic aquí para enviar el mensaje por WhatsApp</a>', unsafe_allow_html=True)
    st.success("Gracias por tu interés. Haz clic en el enlace para enviar el mensaje por WhatsApp.")

# Footer
st.markdown("---")
st.markdown("Desarrollado por **CodeCodix** | Imanol Asolo - Especialista en Soluciones de IA & Automatización Empresarial")
