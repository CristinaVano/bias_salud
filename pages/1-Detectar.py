# pages/1_Detectar.py

import streamlit as st
import pandas as pd
import json
from streamlit_lottie import st_lottie
from ai_core import detectar_patrones_de_inequidad
from config_page import configure_page, animated_title # <--- IMPORTACIÓN MODIFICADA

# Llama a la función que configura la página Y la barra lateral
configure_page(page_title="Detección de Inequidades") # <--- LÍNEA AÑADIDA

@st.cache_data
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f: return json.load(f)
    except: return None

lottie_animation = load_lottiefile("animations/neural_network.json")

# DATOS SIMULADOS
df = pd.DataFrame({
    'Género': ['Hombres', 'Mujeres'], 'Tiempo Medio Diagnóstico (días)': [45, 62]
})

# --- INTERFAZ DE USUARIO ---
animated_title("Detección de Inequidades")
st.subheader("Visión de alto nivel para gestores y responsables de políticas de salud.")
st.markdown("---")

st.subheader("🎯 El Problema Oculto: La Necesidad de una Visión de 360°")
with st.container(border=True):
    st.write("""
    Los sistemas sanitarios generan millones de datos, pero a menudo permanecen en silos, perpetuando **sesgos sistémicos inconscientes**. 
    BIAS actúa como una capa de inteligencia para revelar patrones de inequidad que de otro modo serían invisibles.
    """)

st.subheader("Dashboard de Equidad en Tiempo Real")
col1, col2, col3 = st.columns(3)
with col1: st.metric("Brecha Género (Diag. Cardíaco)", "+37%")
with col2: st.metric("Ratio Prescripción (Mujer/Hombre)", "1.7x")
with col3: st.metric("Reingresos (Baja Renta)", "18%", "7% vs Alta Renta", delta_color="inverse")
st.markdown("---")

st.subheader("Análisis Inteligente por BIAS")
tab1, tab2 = st.tabs(["Ejecutar Análisis", "🧠 ¿Cómo funciona?"])

with tab1:
    st.write("Carga los datos agregados del sistema para que BIAS genere un insight ejecutivo.")
    try:
        with open("demo_data/datos_inequidad.txt", "r") as f: datos_inequidad_texto = f.read()
        datos_input = st.text_area("Fuente de Datos (Simulados):", value=datos_inequidad_texto, height=200, label_visibility="collapsed")
    except FileNotFoundError:
        st.error("Archivo 'demo_data/datos_inequidad.txt' no encontrado.")
        datos_input = ""

    if st.button("Generar Insight Ejecutivo con BIAS", use_container_width=True, type="primary"):
        if datos_input:
            if lottie_animation:
                st_lottie(lottie_animation, height=200, key="lottie_d")
            response_stream = detectar_patrones_de_inequidad(datos_input)
            st.info("Respuesta generada por BIAS:")
            st.write_stream(response_stream)
        else:
            st.warning("No hay datos para analizar.")

with tab2:
    st.subheader("🧠 Arquitectura de Inteligencia: ¿Cómo funciona?")
with st.container(border=True):
    st.markdown(
        """
        La inteligencia de BIAS no reside en un único modelo, sino en una **arquitectura de procesamiento sofisticada y multicapa** que transforma datos crudos y heterogéneos en insights estratégicos. Este es el pipeline:

        #### **Fase 1: Ingesta y Orquestación de Datos Clínicos (ETL Engine)**
        El primer desafío es la diversidad. BIAS se conecta a fuentes de datos heterogéneas, tanto **estructuradas** (EHR, resultados de analíticas) como **no estructuradas** (notas de texto libre, informes de alta). Nuestro motor de ETL (Extract, Transform, Load) realiza:
        - **Normalización y Estandarización:** Unifica formatos y terminologías (ej. mapeo a estándares como CIE-10) para garantizar la coherencia.
        - **Enriquecimiento de Datos:** Cruza información para crear un perfil de paciente de 360°, vinculando datos que antes vivían en silos.
        El resultado es un **Data Lakehouse unificado y gobernado**, la base sobre la que se construye toda la inteligencia.

        #### **Fase 2: Motor de Detección de Patrones (Pattern Recognition Core)**
        Sobre los datos limpios, aplicamos un conjunto de modelos estadísticos y de Machine Learning no supervisado para encontrar "incógnitas conocidas".
        - **Análisis de Cohortes y Clusterización:** Identificamos grupos de pacientes con características similares (clusters) que no son evidentes a simple vista, pero que comparten trayectorias o resultados anómalos.
        - **Detección de Anomalías:** Algoritmos especializados buscan desviaciones significativas en métricas clave (tiempos de espera, tasas de reingreso, pautas de prescripción) que puedan indicar una inequidad sistémica.
        Esta fase no da respuestas, sino que genera **hipótesis estadísticas robustas** y señala dónde mirar.

        #### **Fase 3: Capa de Síntesis Cognitiva (Cognitive Synthesis Layer)**
        Aquí es donde entra en juego el Modelo de Lenguaje Avanzado (LLM), pero no como una simple interfaz de chat. Utilizamos una técnica avanzada llamada **Generación Aumentada por Recuperación (RAG)**.
        - **Contextualización:** El LLM no "imagina" respuestas. Primero, "recupera" los hallazgos estadísticos y los patrones descubiertos en la Fase 2.
        - **Razonamiento Basado en Evidencia:** Utilizando los datos recuperados como contexto, el LLM actúa como un experto, interpretando las correlaciones, explicando las posibles causas de las anomalías y traduciendo los complejos hallazgos numéricos a una **narrativa ejecutiva y comprensible**.
        
        Este proceso sinérgico es lo que nos permite pasar de **datos masivos** a **inteligencia clínica accionable**, garantizando que cada insight generado por BIAS esté anclado en la evidencia contenida en los propios datos del sistema.
        """
    )
