import streamlit as st
import sqlite3

def guest_dashboard(username):
    translations = {
        "es": {
            "title": "Panel de Invitado",
            "info": "¡Bienvenido al demo! Puedes explorar la plataforma y gestionar tus clientes.",
            "actions": ["Ver Clientes", "Agregar Cliente", "Editar Cliente", "Eliminar Cliente"],
            "logout": "Cerrar Sesión",
            "no_customers": "No se encontraron clientes.",
            "add_success": "¡Cliente agregado exitosamente!",
            "edit_success": "¡Cliente actualizado exitosamente!",
            "delete_success": "¡Cliente eliminado exitosamente!",
            "select_action": "Selecciona una acción",
            "your_customers": "Tus Clientes",
            "add_customer_title": "Agregar Nuevo Cliente",
            "edit_customer_title": "Editar Cliente",
            "delete_customer_title": "Eliminar Cliente",
            "name": "Nombre",
            "email": "Correo Electrónico",
            "phone": "Teléfono",
            "notes": "Notas",
            "add_button": "Agregar Cliente",
            "update_button": "Actualizar Cliente",
            "delete_button": "Eliminar Cliente",
            "select_customer_edit": "Selecciona un cliente para editar",
            "select_customer_delete": "Selecciona un cliente para eliminar",
            "name_email_required": "Nombre y Correo Electrónico son obligatorios.",
            "user_not_found": "Usuario no encontrado."
        },
        "en": {
            "title": "Guest Dashboard",
            "info": "Welcome to the demo! You can explore the platform and manage your customers.",
            "actions": ["View Customers", "Add Customer", "Edit Customer", "Delete Customer"],
            "logout": "Logout",
            "no_customers": "No customers found.",
            "add_success": "Customer added successfully!",
            "edit_success": "Customer updated successfully!",
            "delete_success": "Customer deleted successfully!",
            "select_action": "Select an action",
            "your_customers": "Your Customers",
            "add_customer_title": "Add New Customer",
            "edit_customer_title": "Edit Customer",
            "delete_customer_title": "Delete Customer",
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "notes": "Notes",
            "add_button": "Add Customer",
            "update_button": "Update Customer",
            "delete_button": "Delete Customer",
            "select_customer_edit": "Select a customer to edit",
            "select_customer_delete": "Select a customer to delete",
            "name_email_required": "Name and Email are required.",
            "user_not_found": "User not found."
        }
    }

    lang = st.session_state.lang
    t = translations[lang]

    st.subheader(t["title"])
    st.info(t["info"])

    # Connect to the database
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()

    # Ensure the users table exists
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE)''')
    conn.commit()

    # Ensure the guest_customers table exists
    c.execute('''CREATE TABLE IF NOT EXISTS guest_customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    notes TEXT,
                    guest_id INTEGER,
                    FOREIGN KEY(guest_id) REFERENCES users(id))''')
    conn.commit()

    # Get the current guest's ID
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    guest_id = c.fetchone()
    if not guest_id:
        st.error(t["user_not_found"])
        conn.close()
        return
    guest_id = guest_id[0]

    # Action Selector
    action = st.selectbox(t["select_action"], t["actions"])

    if action == t["actions"][0]:  # View Customers
        st.write(f"### {t['your_customers']}")
        customers = c.execute("SELECT id, name, phone, notes FROM guest_customers WHERE guest_id = ?", (guest_id,)).fetchall()
        if customers:
            for customer in customers:
                st.write(f"**{t['name']}:** {customer[1]}")
                st.write(f"**{t['phone']}:** {customer[2]}")
                st.write(f"**{t['notes']}:** {customer[3]}")
                st.write("---")
        else:
            st.info(t["no_customers"])

    elif action == t["actions"][1]:  # Add Customer
        st.write(f"### {t['add_customer_title']}")
        with st.form("Add Customer"):
            name = st.text_input(t["name"])
            email = st.text_input(t["email"])
            phone = st.text_input(t["phone"])
            notes = st.text_area(t["notes"])
            submitted = st.form_submit_button(t["add_button"])
            if submitted:
                if name and email:
                    c.execute("INSERT INTO guest_customers (name, email, phone, notes, guest_id) VALUES (?, ?, ?, ?, ?)",
                              (name, email, phone, notes, guest_id))
                    conn.commit()
                    st.success(t["add_success"])
                    st.rerun()
                else:
                    st.error(t["name_email_required"])

    elif action == t["actions"][2]:  # Edit Customer
        st.write(f"### {t['edit_customer_title']}")
        customers = c.execute("SELECT id, name FROM guest_customers WHERE guest_id = ?", (guest_id,)).fetchall()
        if customers:
            customer_ids = [customer[0] for customer in customers]
            selected_customer_id = st.selectbox(t["select_customer_edit"], customer_ids,
                                                format_func=lambda x: next(c[1] for c in customers if c[0] == x))
            if selected_customer_id:
                selected_customer = c.execute("SELECT name, email, phone, notes FROM guest_customers WHERE id = ?",
                                              (selected_customer_id,)).fetchone()
                with st.form(f"Edit Customer {selected_customer_id}"):
                    name = st.text_input(t["name"], value=selected_customer[0])
                    email = st.text_input(t["email"], value=selected_customer[1])
                    phone = st.text_input(t["phone"], value=selected_customer[2])
                    notes = st.text_area(t["notes"], value=selected_customer[3])
                    submitted = st.form_submit_button(t["update_button"])
                    if submitted:
                        c.execute("UPDATE guest_customers SET name = ?, email = ?, phone = ?, notes = ? WHERE id = ? AND guest_id = ?",
                                  (name, email, phone, notes, selected_customer_id, guest_id))
                        conn.commit()
                        st.success(t["edit_success"])
                        st.rerun()
        else:
            st.info(t["no_customers"])

    elif action == t["actions"][3]:  # Delete Customer
        st.write(f"### {t['delete_customer_title']}")
        customers = c.execute("SELECT id, name FROM guest_customers WHERE guest_id = ?", (guest_id,)).fetchall()
        if customers:
            customer_ids = [customer[0] for customer in customers]
            selected_customer_id = st.selectbox(t["select_customer_delete"], customer_ids,
                                                format_func=lambda x: next(c[1] for c in customers if c[0] == x))
            if st.button(t["delete_button"]):
                c.execute("DELETE FROM guest_customers WHERE id = ?", (selected_customer_id,))
                conn.commit()
                st.success(t["delete_success"])
                st.rerun()
        else:
            st.info(t["no_customers"])

    conn.close()

    # Logout Button
    if st.button(t["logout"]):
        st.session_state.pop("token", None)
        st.session_state.pop("username", None)
        st.rerun()
