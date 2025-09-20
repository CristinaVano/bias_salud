# utils.py (VERSIÓN CORREGIDA PARA ERRORES DE CODIFICACIÓN)

import streamlit as st

def load_svg(filepath):
    """
    Lee un archivo SVG y lo devuelve como una cadena de texto,
    manejando posibles errores de codificación.
    """
    try:
        # Intenta leer con la codificación estándar UTF-8
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Si UTF-8 falla, intenta con 'latin-1', que es más permisivo
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                return f.read()
        except Exception as e:
            # Si ambos fallan, muestra un error claro en la app
            st.error(f"No se pudo leer el icono: {filepath}. Error: {e}")
            return "⚠️" # Devuelve un emoji de error
    except FileNotFoundError:
        # Si el archivo no existe
        st.error(f"Icono no encontrado en la ruta: {filepath}")
        return "⚠️"
