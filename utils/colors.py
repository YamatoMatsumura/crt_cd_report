import streamlit as st
from streamlit_theme import st_theme

def get_theme():
    # theme = st_theme()
    # st.write(theme)
    theme = st.get_option("theme.base")

    if theme == "light":
        return {
            "bg": "#FFFFFF",
            "card_bg": "#F5F7FA",
            "text": "#111827",
            "muted": "#4B5563",
            "grid": "#E5E7EB",
            "primary": "#09396C",
            "accent": "#0272DE"
        }
    else:
        return {
            "bg": "rgba(0,0,0,0)",
            "card_bg": "#21314d",
            "text": "#FFFFFF",
            "muted": "#879EC3",
            "grid": "#30363d",
            "primary": "#0272DE",
            "accent": "#879EC3"
        }