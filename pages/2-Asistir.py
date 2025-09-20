# pages/2_Asistir.py

import streamlit as st
import json
from datetime import datetime
from streamlit_lottie import st_lottie
from ai_core import analizar_riesgo_paciente
from config_page import configure_page, animated_title # <--- IMPORTACIÓN MODIFICADA

# Llama a la función que configura la página Y la barra lateral
configure_page(page_title="Asistencia Clínica") # <--- LÍNEA AÑADIDA

@st.cache_data
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f: return json.load(f)
    except: return None

@st.cache_data
def load_patient_data():
    sujetos = {
        "SUBJ-JG-48M (Depresión Mayor)": {"historial_file": "demo_data/historial_juan_garcia.txt"},
        "SUBJ-ML-35F (Trastorno de Ansiedad)": {"historial_file": "demo_data/historial_maria_lopez.txt"},
        "SUBJ-CR-28M (Posible Bipolaridad)": {"historial_file": "demo_data/historial_carlos_ruiz.txt"}
    }
    for id_sujeto, data in sujetos.items():
        try:
            with open(data["historial_file"], "r") as f:
                sujetos[id_sujeto]["historial"] = f.read()
        except FileNotFoundError:
            st.error(f"Archivo de historial no encontrado para {id_sujeto}")
            sujetos[id_sujeto]["historial"] = "Error al cargar el historial."
    return sujetos

lottie_animation = load_lottiefile("animations/asistir.json")
sujetos_con_datos = load_patient_data()

if 'current_subject_id' not in st.session_state: st.session_state.current_subject_id = list(sujetos_con_datos.keys())[0]
if 'informe_history' not in st.session_state: st.session_state.informe_history = []

lista_demo_sujetos = sorted(list(sujetos_con_datos.keys()) + ["SUBJ-AX-55M", "SUBJ-BV-41F", "SUBJ-CZ-22F"])

animated_title("Asistencia Clínica Aumentada")
st.subheader("El copiloto de IA que potencia la intuición del profesional con datos.")
st.markdown("---")

st.subheader("🎯 El Reto: La Complejidad del Diagnóstico Clínico")
with st.container(border=True):
    st.write("El diagnóstico psiquiátrico es un puzzle complejo. **BIAS actúa como una segunda opinión objetiva**, aumentando las capacidades del profesional con sugerencias basadas en la evidencia.")

st.subheader("Buscador de Pacientes en el Sistema")
sujeto_seleccionado = st.selectbox("Seleccione un sujeto para cargar su historial:", options=lista_demo_sujetos)
if sujeto_seleccionado != st.session_state.current_subject_id:
    st.session_state.current_subject_id = sujeto_seleccionado
    st.rerun()

st.markdown("---")

if st.session_state.current_subject_id in sujetos_con_datos:
    tab1, tab2 = st.tabs(["📝 **Análisis y Generación de Informe**", "📂 **Historial de la Sesión**"])
    with tab1:
        st.subheader(f"Historial Clínico: {st.session_state.current_subject_id}")
        historial_actual = sujetos_con_datos[st.session_state.current_subject_id]["historial"]
        datos_input = st.text_area("Datos del paciente:", value=historial_actual, height=300, label_visibility="collapsed")
        if st.button("Generar Informe de Asistencia con BIAS", use_container_width=True, type="primary"):
            if lottie_animation:
                st_lottie(lottie_animation, height=200, key="lottie_asistir")
            response_stream = analizar_riesgo_paciente(datos_input)
            st.subheader("Panel de Asistencia BIAS")
            st.markdown('<div class="ai-response">', unsafe_allow_html=True)
            full_response = st.write_stream(response_stream)
            st.markdown('</div>', unsafe_allow_html=True)
            informe_nuevo = {"paciente": st.session_state.current_subject_id, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "contenido": full_response}
            st.session_state.informe_history.insert(0, informe_nuevo)
    with tab2:
        st.subheader("Informes Generados en esta Sesión")
        if not st.session_state.informe_history:
            st.info("No se ha generado ningún informe todavía en esta sesión.")
        else:
            for i, informe in enumerate(st.session_state.informe_history):
                with st.expander(f"Informe para **{informe['paciente']}** - {informe['fecha']}"):
                    st.markdown(informe["contenido"])
else:
    st.warning(f"**Datos no disponibles para la demo.** Por favor, seleccione uno de los tres primeros sujetos de la lista.")

st.subheader("🧠 El Cerebro detrás de la Asistencia: ¿Cómo funciona?")
with st.container(border=True):
    st.write(
        """
        Este módulo utiliza un **modelo de lenguaje avanzado (LLM) especializado en literatura médica y guías clínicas (como el DSM-5).**
        #### **1. Extracción y Comprensión Contextual (NLU)**
        BIAS realiza una **Comprensión del Lenguaje Natural (NLU)** para entender el contexto.
        #### **2. Red de Conocimiento Clínico (Clinical Knowledge Graph)**
        Las entidades extraídas se mapean contra una **red de conocimiento** interna.
        #### **3. Generación de Hipótesis y Ponderación de Riesgo**
        El sistema genera un **diagnóstico diferencial priorizado** con sugerencias de tratamiento.
        """
    )
