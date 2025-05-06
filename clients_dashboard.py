import streamlit as st
import sqlite3

# CRM Dashboard for Clients
def clients_dashboard(username):
    translations = {
        "es": {
            "title": "Panel de Clientes",
            "actions": ["Ver Clientes", "Agregar Cliente", "Editar Cliente", "Eliminar Cliente"],
            "manage_customers": "### Gestiona tus Clientes",
            "add_customer": "### Agregar Nuevo Cliente",
            "edit_customer": "### Editar Cliente",
            "delete_customer": "### Eliminar Cliente",
            "client_name": "Nombre del Cliente",
            "contact_info": "Información de Contacto",
            "notes": "Notas",
            "add_button": "Agregar Cliente",
            "update_button": "Actualizar Cliente",
            "delete_button": "Eliminar Cliente",
            "delete_success": "¡Cliente eliminado exitosamente!",
            "add_success": "¡Cliente agregado exitosamente!",
            "edit_success": "¡Cliente actualizado exitosamente!",
            "no_customers": "No se encontraron clientes.",
            "logout": "Cerrar Sesión"
        },
        "en": {
            "title": "Client Dashboard",
            "actions": ["View Customers", "Add Customer", "Edit Customer", "Delete Customer"],
            "manage_customers": "### Manage Customers",
            "add_customer": "### Add New Customer",
            "edit_customer": "### Edit Customer",
            "delete_customer": "### Delete Customer",
            "client_name": "Client Name",
            "contact_info": "Contact Info",
            "notes": "Notes",
            "add_button": "Add Customer",
            "update_button": "Update Customer",
            "delete_button": "Delete Customer",
            "delete_success": "Customer deleted successfully!",
            "add_success": "Customer added successfully!",
            "edit_success": "Customer updated successfully!",
            "no_customers": "No customers found.",
            "logout": "Logout"
        }
    }

    lang = st.session_state.lang
    t = translations[lang]

    st.subheader(t["title"])
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()

    # Get the user ID of the logged-in user
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = c.fetchone()
    if not user_id:
        st.error("User not found.")
        return
    user_id = user_id[0]

    # Action Selector
    action = st.selectbox("Select an action", t["actions"])

    if action == t["actions"][0]:  # View Customers
        st.write(t["manage_customers"])
        customers = c.execute("SELECT id, client_name, contact_info, notes FROM crm WHERE user_id = ?", (user_id,)).fetchall()
        if customers:
            for customer in customers:
                st.write(f"**ID:** {customer[0]}")
                st.write(f"**{t['client_name']}:** {customer[1]}")
                st.write(f"**{t['contact_info']}:** {customer[2]}")
                st.write(f"**{t['notes']}:** {customer[3]}")
                st.write("---")
        else:
            st.info(t["no_customers"])

    elif action == t["actions"][1]:  # Add Customer
        st.write(t["add_customer"])
        with st.form("Add Customer"):
            client_name = st.text_input(t["client_name"])
            contact_info = st.text_input(t["contact_info"])
            notes = st.text_area(t["notes"])
            submitted = st.form_submit_button(t["add_button"])
            if submitted:
                try:
                    c.execute("INSERT INTO crm (client_name, contact_info, notes, user_id) VALUES (?, ?, ?, ?)",
                              (client_name, contact_info, notes, user_id))
                    conn.commit()
                    st.success(t["add_success"])
                except sqlite3.Error as e:
                    st.error(f"An error occurred: {e}")

    elif action == t["actions"][2]:  # Edit Customer
        st.write(t["edit_customer"])
        customers = c.execute("SELECT id, client_name FROM crm WHERE user_id = ?", (user_id,)).fetchall()
        if customers:
            customer_ids = [customer[0] for customer in customers]
            selected_customer_id = st.selectbox("Select a customer to edit", customer_ids, format_func=lambda x: next(c[1] for c in customers if c[0] == x))
            if selected_customer_id:
                selected_customer = c.execute("SELECT client_name, contact_info, notes FROM crm WHERE id = ?", (selected_customer_id,)).fetchone()
                with st.form(f"Edit Customer {selected_customer_id}"):
                    client_name = st.text_input(t["client_name"], value=selected_customer[0])
                    contact_info = st.text_input(t["contact_info"], value=selected_customer[1])
                    notes = st.text_area(t["notes"], value=selected_customer[2])
                    submitted = st.form_submit_button(t["update_button"])
                    if submitted:
                        c.execute("UPDATE crm SET client_name = ?, contact_info = ?, notes = ? WHERE id = ? AND user_id = ?",
                                  (client_name, contact_info, notes, selected_customer_id, user_id))
                        conn.commit()
                        st.success(t["edit_success"])
                        st.rerun()
        else:
            st.info(t["no_customers"])

    elif action == t["actions"][3]:  # Delete Customer
        st.write(t["delete_customer"])
        customers = c.execute("SELECT id, client_name FROM crm WHERE user_id = ?", (user_id,)).fetchall()
        if customers:
            customer_ids = [customer[0] for customer in customers]
            selected_customer_id = st.selectbox("Select a customer to delete", customer_ids, format_func=lambda x: next(c[1] for c in customers if c[0] == x))
            if st.button(t["delete_button"]):
                c.execute("DELETE FROM crm WHERE id = ?", (selected_customer_id,))
                conn.commit()
                st.success(t["delete_success"])
                st.rerun()
        else:
            st.info(t["no_customers"])

    conn.close()

    # Logout Button
    if st.button(t["logout"]):
        st.session_state.pop("token", None)
        st.rerun()
