# config_page.py

import streamlit as st
import time

def configure_page(page_title):
    """
    Función ÚNICA que configura la página y construye los elementos
    comunes de la barra lateral. Streamlit generará los enlaces automáticamente.
    Debe ser llamada al principio de CADA archivo .py de la app.
    """
    st.set_page_config(
        page_title=f"BIAS Health - {page_title}",
        page_icon="images/logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass # No mostramos error si no existe

    # Construir la barra lateral en cada página
    with st.sidebar:
        st.image("images/logo.png")
        st.title("BIAS Health")
        st.caption("Behavioral Intelligence Analysis System")
        st.info("Prototipo funcional con IA en tiempo real (GPT-4o).")
        st.markdown("---")
        st.header("Módulos")
        # Streamlit crea los enlaces del menú automáticamente.

def animated_title(title_text):
    # Esta función está bien y no necesita cambios.
    st.markdown("""
        <style>
        .typewriter-cursor { display: inline-block; background-color: #00F2DE; width: 3px; height: 2.5rem; margin-left: 5px; animation: blink 1s infinite; vertical-align: bottom; }
        @keyframes blink { 50% { background-color: transparent; } }
        </style>
    """, unsafe_allow_html=True)
    title_placeholder = st.empty()
    text = ""
    for char in title_text:
        text += char
        title_placeholder.markdown(f"<h1>{text}<span class='typewriter-cursor'></span></h1>", unsafe_allow_html=True)
        time.sleep(0.05)
    title_placeholder.markdown(f"<h1>{title_text}</h1>", unsafe_allow_html=True)
