import streamlit as st

def mostrar():
    if st.button("🔙 Regresar"):
        st.session_state.pagina = "ProgramaEjemplo"
        st.rerun()

        
    st.title("Aqui ira el inventario disponible")