# pages/3_Agilizar.py

import streamlit as st
import pandas as pd
import json
import time
from streamlit_lottie import st_lottie
from ai_core import generar_resumen_administrativo, generar_pautas_cita
from config_page import configure_page, animated_title # <--- IMPORTACIÓN AÑADIDA

# Llama a la función que configura la página Y la barra lateral
configure_page(page_title="Agilización de Flujos") # <--- LÍNEA AÑADIDA

@st.cache_data
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f: return json.load(f)
    except: return None

@st.cache_data
def load_transcript_data():
    sujetos = {
        "SUBJ-JG-48M (Depresión Mayor)": {"transcripcion_file": "demo_data/transcripcion_juan_garcia.txt"},
        "SUBJ-ML-35F (Trastorno de Ansiedad)": {"transcripcion_file": "demo_data/transcripcion_maria_lopez.txt"},
        "SUBJ-CR-28M (Posible Bipolaridad)": {"transcripcion_file": "demo_data/transcripcion_carlos_ruiz.txt"}
    }
    for id_sujeto, data in sujetos.items():
        try:
            with open(data["transcripcion_file"], "r") as f:
                sujetos[id_sujeto]["transcripcion"] = f.read()
        except FileNotFoundError:
            st.error(f"Archivo de transcripción no encontrado para {id_sujeto}")
            sujetos[id_sujeto]["transcripcion"] = "Error al cargar la transcripción."
    return sujetos

lottie_animation = load_lottiefile("animations/agilizar.json")
sujetos_con_datos = load_transcript_data()

if 'agilizar_subject_id' not in st.session_state: st.session_state.agilizar_subject_id = list(sujetos_con_datos.keys())[0]
if 'agilizar_response' not in st.session_state: st.session_state.agilizar_response = ""
if 'pautas_cita' not in st.session_state: st.session_state.pautas_cita = ""

lista_demo_sujetos = sorted(list(sujetos_con_datos.keys()) + ["SUBJ-AX-55M", "SUBJ-BV-41F", "SUBJ-CZ-22F"])

animated_title("Agilización de Flujos de Trabajo")
st.subheader("Automatización inteligente para devolverle el tiempo a los profesionales.")
st.markdown("---")

st.subheader("🎯 El Ladrón de Tiempo: La Carga Administrativa")
with st.container(border=True):
    st.write(
        """
        Los profesionales sanitarios dedican hasta un **40% de su tiempo** a tareas administrativas. **BIAS ataca directamente esta ineficiencia**, actuando como un escriba inteligente.
        """
    )

st.subheader("Buscador de Sesiones Clínicas")
sujeto_seleccionado = st.selectbox("Seleccione la transcripción de la sesión a resumir:", options=lista_demo_sujetos)

if sujeto_seleccionado != st.session_state.agilizar_subject_id:
    st.session_state.agilizar_subject_id = sujeto_seleccionado
    st.session_state.agilizar_response = ""
    st.session_state.pautas_cita = ""
    st.rerun()

st.markdown("---")

if st.session_state.agilizar_subject_id in sujetos_con_datos:
    st.subheader(f"Transcripción de la Sesión: {st.session_state.agilizar_subject_id}")
    transcripcion_actual = sujetos_con_datos[st.session_state.agilizar_subject_id]["transcripcion"]
    datos_input = st.text_area("Texto de la transcripción:", value=transcripcion_actual, height=300, label_visibility="collapsed")
    
    if st.button("Generar Resumen Clínico con BIAS", use_container_width=True, type="primary"):
        if lottie_animation:
            st_lottie(lottie_animation, height=200, key="lottie_agilizar")
        
        response_stream = generar_resumen_administrativo(datos_input)
        with st.spinner("BIAS está procesando la transcripción..."):
            st.subheader("Resumen para Historial Clínico (EHR)")
            st.markdown('<div class="ai-response">', unsafe_allow_html=True)
            full_response = st.write_stream(response_stream)
            st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.agilizar_response = full_response
            st.rerun()

    if st.session_state.agilizar_response:
        st.subheader("Resumen para Historial Clínico (EHR)")
        st.markdown(f'<div class="ai-response">{st.session_state.agilizar_response}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Planificación de Siguiente Cita")
        
        urgencia_valor = "PRIORITARIA" if "Bipolaridad" in st.session_state.agilizar_subject_id else "Normal"
        st.metric(label="Urgencia recomendada por BIAS", value=urgencia_valor)
        
        if st.button("Generar Pautas para el Paciente", use_container_width=True):
            with st.spinner("🧠 BIAS está redactando las pautas para la próxima cita..."):
                pautas_stream = generar_pautas_cita(st.session_state.agilizar_response)
                # Usamos un placeholder para mostrar la respuesta sin un rerun completo
                pautas_container = st.empty()
                with pautas_container.container():
                    st.markdown('<div class="ai-response">', unsafe_allow_html=True)
                    st.write_stream(pautas_stream)
                    st.markdown('</div>', unsafe_allow_html=True)
                    if st.button("📲 Enviar Cita y Pautas por SMS (Simulado)", use_container_width=True, type="primary"):
                        st.success("✅ Cita confirmada y pautas enviadas al paciente.")
                        time.sleep(2)
                        st.session_state.pautas_cita = "" # Limpiar para la próxima vez
                        st.rerun()
else:
    st.warning(f"**Datos no disponibles para la demo.** Por favor, seleccione uno de los tres primeros sujetos.")

st.subheader("🧠 El Cerebro detrás de la Planificación: ¿Cómo funciona?")
with st.container(border=True):
    st.write(
        """
        Además de resumir, BIAS asiste en la planificación proactiva:
        #### **1. Análisis de Urgencia**
        El sistema recomienda un plazo para la siguiente consulta.
        #### **2. Generación de Pautas Personalizadas**
        Traduce el plan terapéutico a instrucciones claras para el paciente.
        #### **3. Automatización e Integración**
        Permite automatizar el envío de recordatorios y pautas.
        """
    )
