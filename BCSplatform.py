import streamlit as st
import sqlite3
import jwt
import datetime
import bcrypt
from clients_dashboard import clients_dashboard  # Import the clients dashboard module
from admin_dashboard import admin_dashboard  # Import the admin dashboard module
from guest_dashboard import guest_dashboard  # Import guest dashboard
from starter_dashboard import starter_dashboard  # Import starter dashboard
from company_dashboard import company_dashboard  # Import company dashboard
from promoter_dashboard import promoter_dashboard  # Import promoter dashboard
import base64
import os

# Set page config
st.set_page_config(page_title="BCS Platform", page_icon=":guardsman:", layout="wide")

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

# Database setup
def init_db():
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_name TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT,
                    FOREIGN KEY(role) REFERENCES roles(role_name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS crm (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_name TEXT,
                    contact_info TEXT,
                    notes TEXT,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()

    # Populate roles table if empty
    c.execute("SELECT COUNT(*) FROM roles")
    if c.fetchone()[0] == 0:
        roles = ['admin', 'guest', 'starter', 'company', 'promoter']
        c.executemany("INSERT INTO roles (role_name) VALUES (?)", [(role,) for role in roles])
        conn.commit()

    # Check if user_id column exists in crm table
    c.execute("PRAGMA table_info(crm)")
    columns = [column[1] for column in c.fetchall()]
    if "user_id" not in columns:
        c.execute("ALTER TABLE crm ADD COLUMN user_id INTEGER")
        conn.commit()

    conn.close()

# Authentication
def authenticate(username, password):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute('''SELECT u.password, u.role 
                 FROM users u 
                 WHERE u.username = ?''', (username,))
    user = c.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        return {"role": user[1], "username": username}  # Return role and username
    return None

def generate_jwt(username, role):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, "secret", algorithm="HS256")

def verify_jwt(token):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None

# Translations
translations = {
    "es": {
        "title": "Plataforma BCS",
        "login_title": "Iniciar Sesión",
        "login_success": "¡Inicio de sesión exitoso!",
        "login_error": "Usuario o contraseña inválidos.",
        "session_expired": "Sesión expirada. Por favor, inicie sesión nuevamente.",
        "what_is_bcs": "### ¿Qué es un BCS?",
        "bcs_info": "BCS significa :red[**Business Core Solution**], una plataforma diseñada para optimizar la comunicación y colaboración entre usuarios del sistema y clientes.",
        "instructions_title": "¿Cómo usar esta aplicación?",
        "instructions": """
        - **Admins** pueden gestionar usuarios y supervisar la plataforma.
        - **Guests** pueden explorar la plataforma en modo demo.
        - **Starters** pueden gestionar sus datos de clientes con un CRM básico.
        - **Companies** pueden gestionar clientes con características avanzadas de CRM.
        - **Promoters** pueden gestionar promociones y referencias de la app.
        """,
        "register_button": "Registrarse por WhatsApp",
        "pdf_button": "¿Quieres saber más acerca de BCS?"
    },
    "en": {
        "title": "BCS Platform",
        "login_title": "Login",
        "login_success": "Login successful!",
        "login_error": "Invalid username or password.",
        "session_expired": "Session expired. Please log in again.",
        "what_is_bcs": "### What is a BCS?",
        "bcs_info": "BCS stands for :red[**Business Core Solution**], a platform designed to streamline communication and collaboration between system users and customers.",
        "instructions_title": "How to use this app?",
        "instructions": """
        - **Admins** can manage users and oversee the platform.
        - **Guests** can explore the platform in demo mode.
        - **Starters** can manage their own customer data with a basic CRM.
        - **Companies** can manage customers with advanced CRM features.
        - **Promoters** can manage app promotions and referrals.
        """,
        "register_button": "Register via WhatsApp",
        "pdf_button": "Want to know more about BCS?"
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

# Main App
def main():
    st.title(t["title"])
    init_db()

    if "token" not in st.session_state:
        st.session_state["token"] = None

    token = st.session_state["token"]
    if token:
        payload = verify_jwt(token)
        if payload:
            role = payload["role"]
            username = payload["username"]
            if role == "admin":
                admin_dashboard()
            elif role == "guest":
                guest_dashboard(username)  # Pass username to guest_dashboard
            elif role == "starter":
                starter_dashboard(username)
            elif role == "company":
                company_dashboard(username)
            elif role == "promoter":
                promoter_dashboard(username)
        else:
            st.error(t["session_expired"])
            st.session_state["token"] = None
            st.rerun()
    else:
        # Login Screen
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(t["what_is_bcs"])
            st.info(t["bcs_info"])

        with col2:
            with st.expander(t["instructions_title"]):
                st.write(t["instructions"])

            st.markdown(
                f"""
                <style>
                .whatsapp-button {{
                    display: inline-block;
                    background-color: #25D366;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    text-align: center;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 10px;
                }}
                .whatsapp-button:hover {{
                    background-color: #1DA851;
                }}
                </style>
                <a class="whatsapp-button" href="https://wa.me/+5930993513082?text=Hello%20BCS%20team,%20I%20want%20to%20register%20for%20the%20BCS%20platform." target="_blank">{t["register_button"]}</a>
                """,
                unsafe_allow_html=True
            )

            with open("¿Qué es BCS AI.pdf", "rb") as pdf_file:
                pdf_data = pdf_file.read()
                st.download_button(
                    label=t["pdf_button"],
                    data=pdf_data,
                    file_name="¿Qué es BCS AI.pdf",
                    mime="application/pdf"
                )

        st.subheader(t["login_title"])
        with st.form("Login Form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                auth_result = authenticate(username, password)
                if auth_result:
                    st.session_state["token"] = generate_jwt(auth_result["username"], auth_result["role"])
                    st.success(t["login_success"])
                    st.rerun()
                else:
                    st.error(t["login_error"])

if __name__ == "__main__":
    main()
