# BIAS_IA.py

import streamlit as st
from config_page import configure_page

# Llama a la función para configurar la página Y la barra lateral
configure_page(page_title="Bienvenida")

# Contenido de la página
st.title("Bienvenido a BIAS Health")
st.subheader("Misión: Aumentar la Inteligencia Clínica en el Sector Sanitario.")
st.markdown("---")
try:
    st.image("images/foto_portada_bias_salud.png", use_container_width=True)
except Exception:
    pass
