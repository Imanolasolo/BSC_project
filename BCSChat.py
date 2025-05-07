import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI 
from htmlTemplates import css, bot_template, user_template
import os
import base64
import sqlite3

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

# Function to generate a vector store using the text chunks
def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPEN_AI_APIKEY"])
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
        llm = ChatOpenAI(openai_api_key=st.secrets["OPEN_AI_APIKEY"])
        prompt = f"{combined_context}\n\nPregunta: {user_question}\nRespuesta:"
        response = llm.predict(prompt)  # Correct method to generate a response

        # Display the response
        st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)

        # Log the user question and bot response for debugging
        print(f"User: {user_question}")
        print(f"Bot: {response}")

    except Exception as e:
        st.write(f"Se produjo un error al generar la respuesta: {str(e)}")

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title=name, page_icon=":wave:", layout="centered")

    # Function to encode image as base64 to set as background
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # Encode the background image
    img_base64 = get_base64_of_bin_file('background1.jpg')

    # Set the background image using the encoded base64 string
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url('data:image/jpeg;base64,{img_base64}') no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Apply custom CSS styles
    st.write(css, unsafe_allow_html=True)

    # Set the title and header of the app
    st.title("BCS AI Producer Chat")
    st.header(name)
    
    # Display the profile picture and description in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.image('logo1.png', caption=name, width=200)
    with col2:
        description = """
        ### About BCS
        BCS AI Producer is a platform that provides AI solutions for various industries, including finance, healthcare, and more.
        It offers tools for CRMs, predictive modeling, and natural language processing, enabling businesses to leverage AI for improved decision-making and efficiency.
        ### About CodeCodix
        CodeCodix lab is an AI tools builder company which brings business core solutions to various industries, focusing on innovation and efficiency.
        """
        st.markdown(description)

    # Section for interacting with the AI chatbot
    st.write("### Chat with Me, know me and let´s contact!")
    st.info("Doesn´t matter the language, ask anything you need!")

    # Input box for user questions
    user_question = st.text_input("Ask me anything:")
    if user_question:
        handle_user_input(user_question)

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
