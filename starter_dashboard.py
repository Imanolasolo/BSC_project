import streamlit as st
import sqlite3

def starter_dashboard(username):
    translations = {
        "es": {
            "title": "Panel de Starter",
            "actions": ["Ver Clientes", "Agregar Cliente", "Editar Cliente", "Eliminar Cliente"],
            "manage_clients": "### Gestiona tus Clientes",
            "add_client": "### Agregar Nuevo Cliente",
            "edit_client": "### Editar Cliente",
            "delete_client": "### Eliminar Cliente",
            "client_name": "Nombre del Cliente",
            "contact_info": "Información de Contacto",
            "notes": "Notas",
            "add_button": "Agregar Cliente",
            "update_button": "Actualizar Cliente",
            "delete_button": "Eliminar Cliente",
            "delete_success": "¡Cliente eliminado exitosamente!",
            "add_success": "¡Cliente agregado exitosamente!",
            "edit_success": "¡Cliente actualizado exitosamente!",
            "no_clients": "No se encontraron clientes.",
            "logout": "Cerrar Sesión"
        },
        "en": {
            "title": "Starter Dashboard",
            "actions": ["View Clients", "Add Client", "Edit Client", "Delete Client"],
            "manage_clients": "### Manage Your Clients",
            "add_client": "### Add New Client",
            "edit_client": "### Edit Client",
            "delete_client": "### Delete Client",
            "client_name": "Client Name",
            "contact_info": "Contact Info",
            "notes": "Notes",
            "add_button": "Add Client",
            "update_button": "Update Client",
            "delete_button": "Delete Client",
            "delete_success": "Client deleted successfully!",
            "add_success": "Client added successfully!",
            "edit_success": "Client updated successfully!",
            "no_clients": "No clients found.",
            "logout": "Logout"
        }
    }

    lang = st.session_state.lang
    t = translations[lang]

    st.subheader(t["title"])
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()

    # Get user ID
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = c.fetchone()[0]

    # Action Selector
    action = st.selectbox("Select an action", t["actions"])

    if action == t["actions"][0]:  # View Clients
        st.write(t["manage_clients"])
        clients = c.execute("SELECT id, client_name, contact_info, notes FROM crm WHERE user_id = ?", (user_id,)).fetchall()
        if clients:
            for client in clients:
                st.write(f"**ID:** {client[0]}")
                st.write(f"**{t['client_name']}:** {client[1]}")
                st.write(f"**{t['contact_info']}:** {client[2]}")
                st.write(f"**{t['notes']}:** {client[3]}")
                st.write("---")
        else:
            st.info(t["no_clients"])

    elif action == t["actions"][1]:  # Add Client
        st.write(t["add_client"])
        with st.form("Add Client"):
            client_name = st.text_input(t["client_name"])
            contact_info = st.text_input(t["contact_info"])
            notes = st.text_area(t["notes"])
            submitted = st.form_submit_button(t["add_button"])
            if submitted:
                c.execute("INSERT INTO crm (client_name, contact_info, notes, user_id) VALUES (?, ?, ?, ?)",
                          (client_name, contact_info, notes, user_id))
                conn.commit()
                st.success(t["add_success"])

    elif action == t["actions"][2]:  # Edit Client
        st.write(t["edit_client"])
        clients = c.execute("SELECT id, client_name FROM crm WHERE user_id = ?", (user_id,)).fetchall()
        if clients:
            client_ids = [client[0] for client in clients]
            selected_client_id = st.selectbox("Select a client to edit", client_ids, format_func=lambda x: next(c[1] for c in clients if c[0] == x))
            if selected_client_id:
                selected_client = c.execute("SELECT client_name, contact_info, notes FROM crm WHERE id = ?", (selected_client_id,)).fetchone()
                with st.form(f"Edit Client {selected_client_id}"):
                    client_name = st.text_input(t["client_name"], value=selected_client[0])
                    contact_info = st.text_input(t["contact_info"], value=selected_client[1])
                    notes = st.text_area(t["notes"], value=selected_client[2])
                    submitted = st.form_submit_button(t["update_button"])
                    if submitted:
                        c.execute("UPDATE crm SET client_name = ?, contact_info = ?, notes = ? WHERE id = ? AND user_id = ?",
                                  (client_name, contact_info, notes, selected_client_id, user_id))
                        conn.commit()
                        st.success(t["edit_success"])
                        st.rerun()
        else:
            st.info(t["no_clients"])

    elif action == t["actions"][3]:  # Delete Client
        st.write(t["delete_client"])
        clients = c.execute("SELECT id, client_name FROM crm WHERE user_id = ?", (user_id,)).fetchall()
        if clients:
            client_ids = [client[0] for client in clients]
            selected_client_id = st.selectbox("Select a client to delete", client_ids, format_func=lambda x: next(c[1] for c in clients if c[0] == x))
            if st.button(t["delete_button"]):
                c.execute("DELETE FROM crm WHERE id = ?", (selected_client_id,))
                conn.commit()
                st.success(t["delete_success"])
                st.rerun()
        else:
            st.info(t["no_clients"])

    conn.close()

    if st.button(t["logout"]):
        st.session_state.pop("token", None)
        st.rerun()
