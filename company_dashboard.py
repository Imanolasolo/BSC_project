import streamlit as st
import sqlite3

def company_dashboard(username):
    translations = {
        "es": {
            "title": "Panel de Empresa",
            "info": "Gestiona tus usuarios y clientes con características avanzadas de CRM.",
            "manage_users": "### Gestiona Usuarios de la Compañía",
            "manage_clients": "### Gestiona Clientes de los Usuarios",
            "view_users": "### Ver Usuarios de la Compañía",
            "view_clients": "### Ver Clientes de los Usuarios",
            "add_user": "Agregar Usuario",
            "edit_user": "Editar Usuario",
            "delete_user": "Eliminar Usuario",
            "add_client": "Agregar Cliente",
            "edit_client": "Editar Cliente",
            "delete_client": "Eliminar Cliente",
            "user_name": "Nombre del Usuario",
            "client_name": "Nombre del Cliente",
            "contact_info": "Información de Contacto",
            "notes": "Notas",
            "add_button": "Agregar",
            "update_button": "Actualizar",
            "delete_button": "Eliminar",
            "delete_success": "¡Eliminado exitosamente!",
            "add_success": "¡Agregado exitosamente!",
            "edit_success": "¡Actualizado exitosamente!",
            "no_records": "No se encontraron registros.",
            "logout": "Cerrar Sesión"
        },
        "en": {
            "title": "Company Dashboard",
            "info": "Manage your users and clients with advanced CRM features.",
            "manage_users": "### Manage Company Users",
            "manage_clients": "### Manage Clients of Users",
            "view_users": "### View Company Users",
            "view_clients": "### View Clients of Users",
            "add_user": "Add User",
            "edit_user": "Edit User",
            "delete_user": "Delete User",
            "add_client": "Add Client",
            "edit_client": "Edit Client",
            "delete_client": "Delete Client",
            "user_name": "User Name",
            "client_name": "Client Name",
            "contact_info": "Contact Info",
            "notes": "Notes",
            "add_button": "Add",
            "update_button": "Update",
            "delete_button": "Delete",
            "delete_success": "Deleted successfully!",
            "add_success": "Added successfully!",
            "edit_success": "Updated successfully!",
            "no_records": "No records found.",
            "logout": "Logout"
        }
    }

    lang = st.session_state.lang
    t = translations[lang]

    st.subheader(t["title"])
    st.info(t["info"])

    conn = sqlite3.connect("platform.db")
    c = conn.cursor()

    # Ensure the tables have the correct structure
    c.execute('''CREATE TABLE IF NOT EXISTS company_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    company_id INTEGER NOT NULL,
                    created_by INTEGER
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS company_clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_name TEXT NOT NULL,
                    contact_info TEXT,
                    notes TEXT,
                    user_id INTEGER NOT NULL,
                    created_by INTEGER
                )''')

    # Add missing columns if they do not exist
    try:
        c.execute("ALTER TABLE company_users ADD COLUMN created_by INTEGER")
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        c.execute("ALTER TABLE company_clients ADD COLUMN created_by INTEGER")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()

    # Get the ID of the logged-in user with role 'company'
    current_user_id = c.execute("SELECT id FROM users WHERE username = ? AND role = 'company'", (username,)).fetchone()
    if not current_user_id:
        st.error("User not authorized to access this section.")
        return
    current_user_id = current_user_id[0]

    # Selector for managing users or clients
    section = st.selectbox("Select a section", [t["manage_users"], t["manage_clients"]])

    if section == t["manage_users"]:
        st.write(t["manage_users"])
        action = st.selectbox("Select an action", [t["view_users"], t["add_user"], t["edit_user"], t["delete_user"]])

        if action == t["view_users"]:
            st.write(t["view_users"])
            users = c.execute("SELECT user_name FROM company_users WHERE created_by = ?", (current_user_id,)).fetchall()
            if users:
                for user in users:
                    st.write(f"- {user[0]}")
            else:
                st.info(t["no_records"])

        elif action == t["add_user"]:
            with st.form("Add User"):
                user_name = st.text_input(t["user_name"])
                submitted = st.form_submit_button(t["add_button"])
                if submitted:
                    c.execute("INSERT INTO company_users (user_name, company_id, created_by) VALUES (?, ?, ?)", (user_name, 1, current_user_id))
                    conn.commit()
                    st.success(t["add_success"])

        elif action == t["edit_user"]:
            users = c.execute("SELECT id, user_name FROM company_users WHERE created_by = ?", (current_user_id,)).fetchall()
            if users:
                user_ids = [user[0] for user in users]
                selected_user_id = st.selectbox("Select a user to edit", user_ids, format_func=lambda x: next(u[1] for u in users if u[0] == x))
                if selected_user_id:
                    selected_user = c.execute("SELECT user_name FROM company_users WHERE id = ?", (selected_user_id,)).fetchone()
                    with st.form(f"Edit User {selected_user_id}"):
                        user_name = st.text_input(t["user_name"], value=selected_user[0])
                        submitted = st.form_submit_button(t["update_button"])
                        if submitted:
                            c.execute("UPDATE company_users SET user_name = ? WHERE id = ?", (user_name, selected_user_id))
                            conn.commit()
                            st.success(t["edit_success"])

        elif action == t["delete_user"]:
            users = c.execute("SELECT id, user_name FROM company_users WHERE created_by = ?", (current_user_id,)).fetchall()
            if users:
                user_ids = [user[0] for user in users]
                selected_user_id = st.selectbox("Select a user to delete", user_ids, format_func=lambda x: next(u[1] for u in users if u[0] == x))
                if st.button(t["delete_button"]):
                    c.execute("DELETE FROM company_users WHERE id = ?", (selected_user_id,))
                    conn.commit()
                    st.success(t["delete_success"])

    elif section == t["manage_clients"]:
        st.write(t["manage_clients"])
        action = st.selectbox("Select an action", [t["view_clients"], t["add_client"], t["edit_client"], t["delete_client"]])

        if action == t["view_clients"]:
            st.write(t["view_clients"])
            clients = c.execute("SELECT client_name, contact_info FROM company_clients WHERE created_by = ?", (current_user_id,)).fetchall()
            if clients:
                for client in clients:
                    st.write(f"- {client[0]} ({client[1]})")
            else:
                st.info(t["no_records"])

        elif action == t["add_client"]:
            with st.form("Add Client"):
                client_name = st.text_input(t["client_name"])
                contact_info = st.text_input(t["contact_info"])
                notes = st.text_area(t["notes"])
                user_id = st.number_input("User ID", min_value=1, step=1)
                submitted = st.form_submit_button(t["add_button"])
                if submitted:
                    c.execute("INSERT INTO company_clients (client_name, contact_info, notes, user_id, created_by) VALUES (?, ?, ?, ?, ?)",
                              (client_name, contact_info, notes, user_id, current_user_id))
                    conn.commit()
                    st.success(t["add_success"])

        elif action == t["edit_client"]:
            clients = c.execute("SELECT id, client_name FROM company_clients WHERE created_by = ?", (current_user_id,)).fetchall()
            if clients:
                client_ids = [client[0] for client in clients]
                selected_client_id = st.selectbox("Select a client to edit", client_ids, format_func=lambda x: next(c[1] for c in clients if c[0] == x))
                if selected_client_id:
                    selected_client = c.execute("SELECT client_name, contact_info, notes FROM company_clients WHERE id = ?", (selected_client_id,)).fetchone()
                    with st.form(f"Edit Client {selected_client_id}"):
                        client_name = st.text_input(t["client_name"], value=selected_client[0])
                        contact_info = st.text_input(t["contact_info"], value=selected_client[1])
                        notes = st.text_area(t["notes"], value=selected_client[2])
                        submitted = st.form_submit_button(t["update_button"])
                        if submitted:
                            c.execute("UPDATE company_clients SET client_name = ?, contact_info = ?, notes = ? WHERE id = ?",
                                      (client_name, contact_info, notes, selected_client_id))
                            conn.commit()
                            st.success(t["edit_success"])

        elif action == t["delete_client"]:
            clients = c.execute("SELECT id, client_name FROM company_clients WHERE created_by = ?", (current_user_id,)).fetchall()
            if clients:
                client_ids = [client[0] for client in clients]
                selected_client_id = st.selectbox("Select a client to delete", client_ids, format_func=lambda x: next(c[1] for c in clients if c[0] == x))
                if st.button(t["delete_button"]):
                    c.execute("DELETE FROM company_clients WHERE id = ?", (selected_client_id,))
                    conn.commit()
                    st.success(t["delete_success"])

    conn.close()

    if st.button(t["logout"]):
        st.session_state.pop("token", None)
        st.rerun()
