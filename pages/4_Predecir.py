# pages/4_Predecir.py

import streamlit as st
import pandas as pd
import json
import time
from streamlit_lottie import st_lottie
from config_page import configure_page, animated_title # <--- IMPORTACIÓN AÑADIDA

# Llama a la función que configura la página Y la barra lateral
configure_page(page_title="Predicción de Riesgos") # <--- LÍNEA AÑADIDA

@st.cache_data
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f: return json.load(f)
    except: return None

lottie_animation = load_lottiefile("animations/predecir.json")

animated_title("Predicción y Prevención de Riesgos")
st.subheader("De un modelo reactivo a un sistema proactivo de intervención temprana.")
st.markdown("---")

st.subheader("🎯 La Necesidad: Anticiparse a la Crisis")
with st.container(border=True):
    st.write(
        """
        En entornos de alta presión, las crisis de salud mental a menudo se detectan tarde. **BIAS introduce un cambio de paradigma**, permitiendo al personal **intervenir proactivamente**.
        """
    )

st.subheader("Panel de Monitorización de Riesgos en Tiempo Real")
if st.button("Actualizar datos del panel en tiempo real", use_container_width=True, type="primary"):
    animation_container = st.empty()
    with animation_container:
        if lottie_animation:
            st_lottie(lottie_animation, speed=1, loop=True, height=200, key="lottie_predecir")
            st.info("BIAS está re-evaluando los índices de riesgo...")
    time.sleep(3)
    animation_container.empty()
    st.success("✅ Panel de riesgos actualizado.")

data = {'ID Interno': ['#734', '#112', '#801'], 'Módulo': ['C', 'A', 'C'], 'Riesgo Autolítico (IA)': [92, 15, 78], 'Riesgo Suicidio (IA)': [85, 5, 65], 'Riesgo Conflictividad (IA)': [45, 22, 81], 'Tendencia': ['⬆️ ALTA', '➡️ Estable', '⬆️ ALTA']}
df = pd.DataFrame(data)

def colorear_riesgo(val):
    color = 'transparent'
    if isinstance(val, (int, float)):
        if val > 85: color = '#BF616A'
        elif val > 60: color = '#EBCB8B'
    return f'background-color: {color}'

st.dataframe(df.style.applymap(colorear_riesgo, subset=df.select_dtypes(include=['number']).columns), use_container_width=True)

st.markdown("---")
st.subheader("Alertas Predictivas de Alto Impacto")
col1, col2 = st.columns(2, gap="large")
with col1:
    st.error("Alerta Individual (Prioridad Crítica)")
    st.markdown("> #### 🔴 INTERVENCIÓN INMEDIATA (Interno #734)\n> **Riesgo de Suicidio del 85%**. Aumento del 40% en 12h. **Acción:** Activación del protocolo anti-suicidio.")
with col2:
    st.warning("Alerta Colectiva (Prioridad Alta)")
    st.markdown("> #### ⚠️ RIESGO DE BROTE (Módulo C)\n> Índice de tensión ha aumentado un **45%**. **Acción Preventiva:** Refuerzo de la vigilancia.")

st.subheader("🧠 El Cerebro detrás de la Predicción: ¿Cómo funciona?")
with st.container(border=True):
    st.write(
        """
        El motor predictivo de BIAS se basa en la **fusión de múltiples vectores de información**.
        #### **1. Análisis del Lenguaje (NLP) en Tiempo Real**
        #### **2. Detección de Anomalías en el Comportamiento**
        #### **3. Modelos de Clasificación de Riesgo**
        El resultado es un **"índice de riesgo" compuesto y dinámico**.
        """
    )
