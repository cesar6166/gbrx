#Cerebro del programa
import streamlit as st
import Login
import ProgramaEjemplo
import BD
import entregas

# Configurar la página
st.set_page_config(
    page_title="MRO",
    page_icon="LOGO.jpeg",  
    layout="wide"
)

def main():
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    if 'usuario' not in st.session_state:
        st.session_state.usuario = ""
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "Login"

    if st.session_state.pagina == "Login":
        Login.mostrar()
    elif st.session_state.pagina == "ProgramaEjemplo":
        ProgramaEjemplo.mostrar()
    elif st.session_state.pagina == "BD":
        BD.base_de_datos()
    elif st.session_state.pagina == "entregas":
        entregas.Entregas()

if __name__ == "__main__":
    main()
