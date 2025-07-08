# bcs_landing.py

import streamlit as st
from PIL import Image
import base64
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI 
from htmlTemplates import css, bot_template, user_template
import os
import sqlite3

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

# Set your name for the AIProfileVCard
name = 'CodeCodix AI lab'

# Function to extract text from a PDF file
def get_pdf_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text = ""
    # Iterate through each page and extract text
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to split the extracted text into manageable chunks for processing
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_openai_key():
    # Busca la API key en todas las variantes posibles y muestra el error con las claves encontradas
    posibles = [
        "OPENAI_API_KEY",
        "OPEN_AI_APIKEY",
        "openai_api_key",
        "open_ai_apikey"
    ]
    for k in posibles:
        if k in st.secrets:
            return st.secrets[k]
    st.error(
        "No se encontró la clave de OpenAI en secrets.toml. "
        "Asegúrate de que la clave esté definida como OPENAI_API_KEY, OPEN_AI_APIKEY, openai_api_key o open_ai_apikey. "
        f"Claves encontradas: {list(st.secrets.keys())}"
    )
    st.stop()

# Function to generate a vector store using the text chunks
def get_vector_store(text_chunks):
    openai_key = get_openai_key()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to create a context from the database
def create_db_context(db_path):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Get all table names in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            return "No se encontraron tablas en la base de datos."

        # Extract and format data from each table
        context = ""
        for table in tables:
            table_name = table[0]
            context += f"\n### Table: {table_name} ###\n"
            try:
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()

                # Get column names for the table
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in cursor.fetchall()]
                context += ", ".join(columns) + "\n"  # Add column headers

                # Add rows of data
                for row in rows:
                    context += ", ".join(map(str, row)) + "\n"
            except sqlite3.OperationalError as e:
                context += f"Error al acceder a la tabla {table_name}: {str(e)}\n"

        connection.close()
        return context

    except Exception as e:
        return f"Se produjo un error inesperado al procesar la base de datos: {str(e)}"

# Function to create a combined context from the PDF and database
def create_combined_context(pdf_path, db_path):
    # Extract text from the PDF
    pdf_text = get_pdf_text(pdf_path)

    # Extract data from the database
    db_context = create_db_context(db_path)

    # Combine the PDF text and database context
    combined_context = f"### Contexto del PDF ###\n{pdf_text}\n\n### Contexto de la Base de Datos ###\n{db_context}"
    return combined_context

# Function to handle user input and generate responses
def handle_user_input(user_question):
    # Paths to the PDF and database
    pdf_path = os.path.join(os.getcwd(), "¿Qué es BCS AI.pdf")
    db_path = os.path.join(os.getcwd(), "platform.db")

    # Create the combined context
    combined_context = create_combined_context(pdf_path, db_path)

    # Use the language model to generate a response
    try:
        openai_key = get_openai_key()
        llm = ChatOpenAI(openai_api_key=openai_key)
        prompt = f"{combined_context}\n\nPregunta: {user_question}\nRespuesta:"
        response = llm.predict(prompt)  # Correct method to generate a response

        # Display the response
        st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)

        # Log the user question and bot response for debugging
        print(f"User: {user_question}")
        print(f"Bot: {response}")

    except Exception as e:
        st.write(f"Se produjo un error al generar la respuesta: {str(e)}")

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
use_cases = t["use_cases"]
col1, col2, col3 = st.columns(3)
if len(use_cases) > 0:
    with col1:
        st.info(use_cases[0])
if len(use_cases) > 1:
    with col2:
        st.info(use_cases[1])
if len(use_cases) > 2:
    with col3:
        st.info(use_cases[2])

# Call to action
st.markdown(f"## {t['cta_title']}")
st.success(t["cta_demo"])
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(t["cta_contact"])
with col2:
    st.markdown(t["cta_email"])
with col3:
    # Traducción del título y placeholder del chatbot según idioma
    chat_expander_title = {
        "es": "Chatea con nosotros",
        "en": "Chat with us"
    }
    chat_placeholder = {
        "es": "Dinos quién eres y qué haces y podremos ayudarte mejor:",
        "en": "Tell us who you are and what you do so we can help you better:"
    }
    user_question = st.text_input(chat_placeholder[lang])
    if user_question:
        handle_user_input(user_question)

# Promoter button
promoter_button_text = {
    "es": "¿Quieres hacer negocio siendo promotor de BCS?",
    "en": "Do you want to do business as a BCS promoter?"
}
promoter_url = "https://bcspromoter-landing.streamlit.app/?embed_options=dark_theme"
if st.button(promoter_button_text[lang], key=f"promoter_btn_{lang}"):
    st.markdown(f'<a href="{promoter_url}" target="_blank">{promoter_button_text[lang]}</a>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption(t["footer"])
st.markdown(t["copyright"])
