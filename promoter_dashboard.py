import streamlit as st
import sqlite3
import webbrowser

def create_promoter_clients_table():
    conn = sqlite3.connect('platform.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promoter_clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            promoter_id TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_promoter_clients_table()

def promoter_dashboard(username):
    translations = {
        "es": {
            "title": "Panel de Promotor",
            "info": "Promociona la app y rastrea tus referencias.",
            "coming_soon": "Próximamente: Seguimiento de referencias y análisis.",
            "logout": "Cerrar Sesión",
            "manage_clients": "Gestiona tus Clientes",
            "add_client": "Agregar Cliente",
            "view_clients": "Ver Clientes",
            "edit_client": "Editar Cliente",
            "delete_client": "Eliminar Cliente",
            "add_new_client": "Agregar un Nuevo Cliente",
            "name": "Nombre",
            "email": "Correo Electrónico",
            "phone": "Teléfono",
            "client_added": "¡Cliente agregado exitosamente!",
            "your_clients": "Tus Clientes",
            "edit_a_client": "Editar un Cliente",
            "select_client_edit": "Selecciona un cliente para editar:",
            "client_updated": "¡Cliente actualizado exitosamente!",
            "delete_a_client": "Eliminar un Cliente",
            "select_client_delete": "Selecciona un cliente para eliminar:",
            "client_deleted": "¡Cliente eliminado exitosamente!",
            "promotion_tools": "Herramientas de Promoción",
            "send_whatsapp": "Enviar un Mensaje de WhatsApp a un Cliente",
            "select_client": "Selecciona un cliente:",
            "message": "Mensaje",
            "send_message": "Enviar Mensaje de WhatsApp",
            "whatsapp_success": "El enlace de WhatsApp se abrió en tu navegador. Completa la acción allí.",
            "more_tools": "Próximamente: ¡Más herramientas!",
            "select_action": "Selecciona una acción:"
        },
        "en": {
            "title": "Promoter Dashboard",
            "info": "Promote the app and track your referrals.",
            "coming_soon": "Coming soon: Referral tracking and analytics.",
            "logout": "Logout",
            "manage_clients": "Manage Your Clients",
            "add_client": "Add Client",
            "view_clients": "View Clients",
            "edit_client": "Edit Client",
            "delete_client": "Delete Client",
            "add_new_client": "Add a New Client",
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "client_added": "Client added successfully!",
            "your_clients": "Your Clients",
            "edit_a_client": "Edit a Client",
            "select_client_edit": "Select a client to edit:",
            "client_updated": "Client updated successfully!",
            "delete_a_client": "Delete a Client",
            "select_client_delete": "Select a client to delete:",
            "client_deleted": "Client deleted successfully!",
            "promotion_tools": "Promotion Tools",
            "send_whatsapp": "Send a WhatsApp Message to a Client",
            "select_client": "Select a client:",
            "message": "Message",
            "send_message": "Send WhatsApp Message",
            "whatsapp_success": "WhatsApp message link opened in your browser. Complete the action there.",
            "more_tools": "Coming soon: More tools!",
            "select_action": "Select an action:"
        }
    }

    lang = st.session_state.lang
    t = translations[lang]

    st.subheader(t["title"])
    st.info(t["info"])
    st.write(t["coming_soon"])

    st.subheader(t["manage_clients"])

    conn = sqlite3.connect('platform.db')
    cursor = conn.cursor()

    # Selector for CRUD operations
    crud_option = st.selectbox(t["select_action"], [t["add_client"], t["view_clients"], t["edit_client"], t["delete_client"]])

    if crud_option == t["add_client"]:
        with st.form("add_client_form"):
            st.write(t["add_new_client"])
            name = st.text_input(t["name"])
            email = st.text_input(t["email"])
            phone = st.text_input(t["phone"])
            submitted = st.form_submit_button(t["add_client"])

            if submitted and name:
                cursor.execute(
                    "INSERT INTO promoter_clients (promoter_id, name, email, phone) VALUES (?, ?, ?, ?)",
                    (username, name, email, phone)
                )
                conn.commit()
                st.success(t["client_added"])

    elif crud_option == t["view_clients"]:
        st.write(t["your_clients"])
        cursor.execute("SELECT id, name, email, phone FROM promoter_clients WHERE promoter_id = ?", (username,))
        clients = cursor.fetchall()

        for client in clients:
            st.write(f"**{client[1]}** - {client[2]} - {client[3]}")

    elif crud_option == t["edit_client"]:
        st.write(t["edit_a_client"])
        cursor.execute("SELECT id, name FROM promoter_clients WHERE promoter_id = ?", (username,))
        clients = cursor.fetchall()
        client_dict = {client[1]: client[0] for client in clients}
        selected_client = st.selectbox(t["select_client_edit"], list(client_dict.keys()))

        if selected_client:
            client_id = client_dict[selected_client]
            cursor.execute("SELECT name, email, phone FROM promoter_clients WHERE id = ?", (client_id,))
            client_data = cursor.fetchone()

            with st.form(f"edit_client_form_{client_id}"):
                new_name = st.text_input(t["name"], value=client_data[0])
                new_email = st.text_input(t["email"], value=client_data[1])
                new_phone = st.text_input(t["phone"], value=client_data[2])
                update_submitted = st.form_submit_button(t["edit_client"])

                if update_submitted:
                    cursor.execute(
                        "UPDATE promoter_clients SET name = ?, email = ?, phone = ? WHERE id = ?",
                        (new_name, new_email, new_phone, client_id)
                    )
                    conn.commit()
                    st.success(t["client_updated"])

    elif crud_option == t["delete_client"]:
        st.write(t["delete_a_client"])
        cursor.execute("SELECT id, name FROM promoter_clients WHERE promoter_id = ?", (username,))
        clients = cursor.fetchall()
        client_dict = {client[1]: client[0] for client in clients}
        selected_client = st.selectbox(t["select_client_delete"], list(client_dict.keys()))

        if selected_client:
            client_id = client_dict[selected_client]
            if st.button(f"{t['delete_client']} {selected_client}"):
                cursor.execute("DELETE FROM promoter_clients WHERE id = ?", (client_id,))
                conn.commit()
                st.success(t["client_deleted"])

    conn.close()

    st.subheader(t["promotion_tools"])

    conn = sqlite3.connect('platform.db')
    cursor = conn.cursor()

    # Fetch clients for dropdown
    cursor.execute("SELECT id, name, phone FROM promoter_clients WHERE promoter_id = ?", (username,))
    clients = cursor.fetchall()
    client_dict = {client[1]: client[2] for client in clients}

    # WhatsApp messaging tool
    with st.form("whatsapp_form"):
        st.write(t["send_whatsapp"])
        selected_client = st.selectbox(t["select_client"], list(client_dict.keys()))
        message = st.text_area(t["message"])
        whatsapp_submitted = st.form_submit_button(t["send_message"])

        if whatsapp_submitted and selected_client and message:
            phone = client_dict[selected_client]
            whatsapp_url = f"https://wa.me/{phone}?text={message}"
            webbrowser.open(whatsapp_url)
            st.success(t["whatsapp_success"])

    conn.close()

    st.write(t["more_tools"])

    if st.button(t["logout"]):
        st.session_state.pop("token", None)
        st.rerun()
