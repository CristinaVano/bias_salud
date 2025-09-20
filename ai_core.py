# ai_core.py (CORREGIDO)

import os
from openai import OpenAI
import streamlit as st
import markdown2
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env si existe (para desarrollo local)
load_dotenv()

# La forma correcta y segura de obtener la clave de API
api_key = st.secrets.get("OPENAI_API_KEY")

# Inicializa el cliente de OpenAI solo si la clave existe
client = OpenAI(api_key=api_key) if api_key else None

def get_ai_response_stream(system_prompt, user_input):
    if not client:
        yield "Error: Clave de API de OpenAI no configurada o inválida. Por favor, configúrala en los 'Secrets' de la aplicación."
        return
    try:
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            stream=True,
            temperature=0.5 # Añadimos un poco de variabilidad controlada
        )
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""
    except Exception as e:
        yield f"Ha ocurrido un error al contactar con el servicio de IA: {e}"

# (El resto de tus funciones se mantienen 100% intactas, son perfectas)
def detectar_patrones_de_inequidad(datos_demograficos):
    system_prompt = "Eres un analista de IA para gestores de salud pública. Analiza los datos y genera un **INSIGHT DE IA:** directo y cuantitativo sobre la correlación más significativa y preocupante."
    return get_ai_response_stream(system_prompt, datos_demograficos)

def analizar_riesgo_paciente(historial_clinico):
    system_prompt = """
    Eres un asistente de IA para psiquiatras (DSM-5). Analiza el historial y devuelve un análisis conciso en TRES PÁRRAFOS SEPARADOS.

    1.  **ALERTA DE RIESGO:** Empieza con este título en negrita. Describe el riesgo principal, su nivel (Bajo, Moderado, Alto, Crítico) y una probabilidad porcentual. Justifica brevemente.
    2.  **SUGERENCIA DE TRATAMIENTO:** Empieza con este título en negrita. Sugiere un plan de acción farmacológico o terapéutico claro y justificado.
    3.  **DIAGNÓSTICO DIFERENCIAL:** Empieza con este título en negrita. Enumera 2 o 3 posibles diagnósticos del DSM-5, explicando la compatibilidad con los síntomas.

    NO USES LISTAS NI VIÑETAS. Escribe en párrafos fluidos y cohesionados.
    """
    return get_ai_response_stream(system_prompt, historial_clinico)

def generar_resumen_administrativo(transcripcion):
    system_prompt = """
    Eres un asistente de IA médico, experto en procesar transcripciones y generar resúmenes clínicos concisos para EHR.
    Tu tarea es extraer la información clave y presentarla en un formato claro usando Markdown.
    El título principal debe ser 'Resumen Clínico (Generado por BIAS)' en negrita.
    Los siguientes puntos deben ser una lista sin ordenar: Paciente, Periodo, Síntomas Clave, Posible Diagnóstico, Plan.
    """
    return get_ai_response_stream(system_prompt, transcripcion)

def generar_pautas_cita(resumen_clinico):
    system_prompt = """
    Eres un asistente de IA para la gestión de pacientes. A partir del siguiente resumen clínico, tu tarea es generar un bloque de texto conciso con "Pautas Preparatorias para la Próxima Cita".
    El texto debe ser claro, directo y orientado al paciente. NO incluyas ninguna etiqueta de formato como 'markdown' o ```.
    La salida debe empezar directamente con el título "Pautas Preparatorias para la Próxima Cita" en negrita.
    """
    user_prompt = f"Genera las pautas basadas en este resumen:\n\n{resumen_clinico}"
    return get_ai_response_stream(system_prompt, user_prompt)

def format_ai_response_to_html(text):
    html = markdown2.markdown(text, extras=["cuddled-lists", "break-on-newline"])
    return html
