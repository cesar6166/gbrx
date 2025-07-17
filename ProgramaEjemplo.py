#ProgramaEjemplo = Programa Principal
import streamlit as st

def mostrar():
    #Encabezado
    col1, col2 = st.columns([1, 5])

    with col1:
        st.title("Menú")
        
    with col2:
        st.image("LOGO.jpeg", width=100)

    # Mostrar mensaje de bienvenida si el usuario está autenticado
    if st.session_state.get("autenticado", False):
        st.success(f"¡Bienvenido, {st.session_state.usuario}!")

    if st.button("Items"):
        st.session_state.pagina = "BD"
        st.rerun()
    
    if st.button("Entregas"):
        st.session_state.pagina = "entregas"
        st.rerun()

    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.session_state.usuario = ""
        st.session_state.pagina = "Login"
        st.rerun()
