import streamlit as st
import sqlite3
import bcrypt

def admin_dashboard():
    translations = {
        "es": {
            "title": "Panel de Administrador",
            "manage_users": "### Gestiona Usuarios",
            "add_user": "### Agregar Nuevo Usuario",
            "edit_user": "### Modificar Usuario",
            "username": "Nombre de Usuario",
            "password": "Contraseña",
            "role": "Rol",
            "add_button": "Agregar Usuario",
            "edit_button": "Modificar Usuario",
            "delete_success": "¡Usuario eliminado exitosamente!",
            "add_success": "¡Usuario agregado exitosamente!",
            "edit_success": "¡Usuario modificado exitosamente!",
            "logout": "Cerrar Sesión",
            "manage_roles": "### Gestiona Roles",
            "add_role": "### Agregar Nuevo Rol",
            "edit_role": "### Modificar Rol",
            "role_name": "Nombre del Rol",
            "role_add_success": "¡Rol agregado exitosamente!",
            "role_edit_success": "¡Rol modificado exitosamente!",
            "role_delete_success": "¡Rol eliminado exitosamente!",
            "user_action_selector": "Seleccionar Acción de Usuario",
            "user_action_options": ["Ver Usuarios", "Agregar Usuario", "Modificar Usuario", "Eliminar Usuario"],
            "role_action_selector": "Seleccionar Acción de Rol",
            "role_action_options": ["Ver Roles", "Agregar Rol", "Modificar Rol", "Eliminar Rol"],
            "company": "Compañía",
            "city": "Ciudad",
            "country": "País",
        },
        "en": {
            "title": "Admin Dashboard",
            "manage_users": "### Manage Users",
            "add_user": "### Add New User",
            "edit_user": "### Edit User",
            "username": "Username",
            "password": "Password",
            "role": "Role",
            "add_button": "Add User",
            "edit_button": "Edit User",
            "delete_success": "User deleted successfully!",
            "add_success": "User added successfully!",
            "edit_success": "User edited successfully!",
            "logout": "Logout",
            "manage_roles": "### Manage Roles",
            "add_role": "### Add New Role",
            "edit_role": "### Edit Role",
            "role_name": "Role Name",
            "role_add_success": "Role added successfully!",
            "role_edit_success": "Role edited successfully!",
            "role_delete_success": "Role deleted successfully!",
            "user_action_selector": "Select User Action",
            "user_action_options": ["View Users", "Add User", "Edit User", "Delete User"],
            "role_action_selector": "Select Role Action",
            "role_action_options": ["View Roles", "Add Role", "Edit Role", "Delete Role"]
        }
    }

    lang = st.session_state.get("lang", "en")
    t = translations[lang]

    st.subheader(t["title"])
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()

    # Ensure the 'users' table has the new fields
    existing_columns = [row[1] for row in c.execute("PRAGMA table_info(users)").fetchall()]
    if 'email' not in existing_columns:
        c.execute("ALTER TABLE users ADD COLUMN email TEXT")
    if 'company' not in existing_columns:
        c.execute("ALTER TABLE users ADD COLUMN company TEXT")
    if 'city' not in existing_columns:
        c.execute("ALTER TABLE users ADD COLUMN city TEXT")
    if 'country' not in existing_columns:
        c.execute("ALTER TABLE users ADD COLUMN country TEXT")
    if 'address' not in existing_columns:
        c.execute("ALTER TABLE users ADD COLUMN address TEXT")
    conn.commit()

    # Selector for User Management
    st.markdown(f"<h2 style='color: red;'>{t['user_action_selector']}</h2>", unsafe_allow_html=True)
    user_action = st.selectbox("", t["user_action_options"])

    # Update the 'View Users' section to display new fields
    if user_action == t["user_action_options"][0]:
        st.write(t["manage_users"])
        users = c.execute("SELECT u.id, u.username, u.email, u.company, u.city, u.country, u.address, u.role FROM users u").fetchall()
        st.table([
            {
                "ID": user[0],
                t["username"]: user[1],
                "Email": user[2],
                "Company": user[3],
                "City": user[4],
                "Country": user[5],
                "Address": user[6],
                t["role"]: user[7]
            } for user in users
        ])

    # Update the 'Add User' section to include new fields
    elif user_action == t["user_action_options"][1]:
        with st.form("Add User"):
            st.write(t["add_user"])
            username = st.text_input(t["username"])
            password = st.text_input(t["password"], type="password")
            email = st.text_input(t["email"] if "email" in t else "Email")
            company = st.text_input(t["company"] if "company" in t else "Company")
            city = st.text_input(t["city"] if "city" in t else "City")
            country = st.text_input(t["country"] if "country" in t else "Country")
            address = st.text_input(t["address"] if "address" in t else "Address")
            roles = c.execute("SELECT role_name FROM roles").fetchall()
            role = st.selectbox(t["role"], [r[0] for r in roles])
            submitted = st.form_submit_button(t["add_button"])
            if submitted:
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                try:
                    c.execute(
                        "INSERT INTO users (username, password, email, company, city, country, address, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (username, hashed_pw, email, company, city, country, address, role)
                    )
                    conn.commit()
                    st.success(t["add_success"])
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Username already exists.")

    # Update the 'Edit User' section to include new fields
    elif user_action == t["user_action_options"][2]:
        st.write(t["edit_user"])
        users = c.execute("SELECT id, username FROM users").fetchall()
        user_to_edit = st.selectbox("Select User to Edit", [f"{u[0]} - {u[1]}" for u in users])
        user_id = int(user_to_edit.split(" - ")[0])
        new_username = st.text_input(t["username"])
        new_password = st.text_input(t["password"], type="password")
        new_email = st.text_input("Email")
        new_company = st.text_input("Company")
        new_city = st.text_input("City")
        new_country = st.text_input("Country")
        new_address = st.text_input("Address")
        roles = c.execute("SELECT role_name FROM roles").fetchall()
        new_role = st.selectbox(t["role"], [r[0] for r in roles])
        if st.button(t["edit_button"], key=f"edit_user_{user_id}"):
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            c.execute(
                "UPDATE users SET username = ?, password = ?, email = ?, company = ?, city = ?, country = ?, address = ?, role = ? WHERE id = ?",
                (new_username, hashed_pw, new_email, new_company, new_city, new_country, new_address, new_role, user_id)
            )
            conn.commit()
            st.success(t["edit_success"])

    elif user_action == t["user_action_options"][3]:
        st.write("### Delete User")
        users = c.execute("SELECT id, username FROM users").fetchall()
        user_to_delete = st.selectbox("Select User to Delete", [f"{u[0]} - {u[1]}" for u in users])
        user_id = int(user_to_delete.split(" - ")[0])
        if st.button("Confirm Delete", key=f"confirm_delete_user_{user_id}"):
            c.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            st.success("User deleted successfully!")

    # Selector for Role Management
    st.markdown(f"<h2 style='color: red;'>{t['role_action_selector']}</h2>", unsafe_allow_html=True)
    role_action = st.selectbox("", t["role_action_options"])

    if role_action == t["role_action_options"][0]:
        st.write(t["manage_roles"])
        roles = c.execute("SELECT id, role_name FROM roles").fetchall()
        st.table([{"ID": role[0], t["role_name"]: role[1]} for role in roles])

    elif role_action == t["role_action_options"][1]:
        with st.form("Add Role"):
            st.write(t["add_role"])
            new_role = st.text_input(t["role_name"])
            submitted = st.form_submit_button(t["add_button"])
            if submitted:
                try:
                    c.execute("INSERT INTO roles (role_name) VALUES (?)", (new_role,))
                    conn.commit()
                    st.success(t["role_add_success"])
                except sqlite3.IntegrityError:
                    st.error("Role already exists.")

    elif role_action == t["role_action_options"][2]:
        st.write(t["edit_role"])
        roles = c.execute("SELECT id, role_name FROM roles").fetchall()
        role_to_edit = st.selectbox("Select Role to Edit", [f"{r[0]} - {r[1]}" for r in roles])
        role_id = int(role_to_edit.split(" - ")[0])
        new_role_name = st.text_input(t["role_name"])
        if st.button(t["edit_button"], key=f"edit_role_{role_id}"):
            c.execute("UPDATE roles SET role_name = ? WHERE id = ?", (new_role_name, role_id))
            conn.commit()
            st.success(t["role_edit_success"])

    elif role_action == t["role_action_options"][3]:
        st.write("### Delete Role")
        roles = c.execute("SELECT id, role_name FROM roles").fetchall()
        role_to_delete = st.selectbox("Select Role to Delete", [f"{r[0]} - {r[1]}" for r in roles])
        role_id = int(role_to_delete.split(" - ")[0])
        if st.button("Confirm Delete", key=f"confirm_delete_role_{role_id}"):
            c.execute("DELETE FROM roles WHERE id = ?", (role_id,))
            conn.commit()
            st.success("Role deleted successfully!")

    conn.close()

    # Logout Button
    if st.button(t["logout"]):
        st.session_state.pop("token", None)
        st.rerun()
