import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import Login
import ProgramaEjemplo
import catalagos
import entregas
import InventarioDisponible

# Obtener el ancho de la ventana
window_width = streamlit_js_eval(js_expressions="window.innerWidth", key="WIDTH")

# Configurar la página según el ancho
if window_width and window_width < 768:
    st.set_page_config(
        page_title="MRO",
        page_icon="LOGO.jpeg",
        layout="centered"
    )
else:
    st.set_page_config(
        page_title="MRO",
        page_icon="LOGO.jpeg",
        layout="wide"
    )

# Lógica principal
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
    elif st.session_state.pagina == "catalagos":
        catalagos.items()
    elif st.session_state.pagina == "entregas":
        entregas.Entregas()
    elif st.session_state.pagina == "InventarioDisponible":
        InventarioDisponible.mostrar()

if __name__ == "__main__":
    main()
