#Pagina de login
import streamlit as st
import sqlite3
import bcrypt
import os


# Inicializar variables de sesión
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario' not in st.session_state:
    st.session_state.usuario = ""
if 'pagina' not in st.session_state:
    st.session_state.pagina = "Login"

DB_NAME = 'Warehouse.db'

def crear_base_datos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contraseña_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def registrar_usuario(usuario, contraseña):
    contraseña_hash = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt())
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contraseña_hash) VALUES (?, ?)", (usuario, contraseña_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def validar_usuario(usuario, contraseña):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT contraseña_hash FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return bcrypt.checkpw(contraseña.encode(), resultado[0])
    return False

def mostrar():
    
    #Creamos la base de datos por si no llega a existir

    if not os.path.exists(DB_NAME):
        crear_base_datos()
    else:
        # Asegura que la tabla exista aunque el archivo ya exista
        crear_base_datos()
    
    st.title("Inicio de Sesión")

    pestaña = st.radio("Selecciona una opción:", ("Iniciar sesión", "Registrarse"))

    if pestaña == "Iniciar sesión":
        st.subheader("Iniciar Sesión")
        st.image("GREENBRIERLOGO.png", width=200)
        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            contraseña = st.text_input("Contraseña", type="password")
            iniciar = st.form_submit_button("Iniciar sesión")

            if iniciar:
                if validar_usuario(usuario, contraseña):
                    st.session_state.autenticado = True
                    st.session_state.usuario = usuario
                    st.session_state.pagina = "ProgramaEjemplo"
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")

    else:
        st.subheader("Registro de Usuario")
        st.image("GREENBRIERLOGO.png", width=200)
        clave_acceso = st.text_input("Contraseña de acceso", type="password")

        if clave_acceso == "GundersonMRO2025":
            with st.form("registro_form"):
                nuevo_usuario = st.text_input("Nuevo usuario")
                nueva_contraseña = st.text_input("Nueva contraseña", type="password")
                registrar = st.form_submit_button("Registrar")

            if registrar:
                if not nuevo_usuario or not nueva_contraseña:
                    st.warning("Por favor, completa todos los campos.")
                else:
                    if registrar_usuario(nuevo_usuario, nueva_contraseña):
                        st.success("Usuario registrado correctamente.")
                    else:
                        st.error("El usuario ya existe.")
        elif clave_acceso:
            st.error("Contraseña incorrecta.")

