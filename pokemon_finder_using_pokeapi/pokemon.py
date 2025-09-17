import streamlit as st
import requests
import certifi

st.set_page_config(page_title =" Pokemon Finder", page_icon="✨", layout= "centered", initial_sidebar_state = "collapsed")

BASE_URL = "https://pokeapi.co/api/v2"
REQUEST_TIMEOUT = 15

TYPE_COLORS = {
    "normal": "#A8A878", "fire": "#F08030", "water": "#6890F0",
    "electric": "#F8D030", "grass": "#78C850", "ice": "#98D8D8",
    "fighting": "#C03028", "poison": "#A040A0", "ground": "#E0C068",
    "flying": "#A890F0", "psychic": "#F85888", "bug": "#A8B820",
    "rock": "#B8A038", "ghost": "#705898", "dragon": "#7038F8",
    "dark": "#705848", "steel": "#B8B8D0", "fairy": "#EE99AC"
}

@st.cache_resource
def get_session():
    session = requests.Session()
    session.headers.update({"User-Agent": "PokemonSearch/1.0"})
    session.verify = certifi.where()
    return session

session = get_session()

def fetch_pokemon_data(name_or_id):
    try:
        url = f"{BASE_URL}/pokemon/{name_or_id.lower()}"
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None
def get_sprite_url():
    pass

st.markdown("""
<div class="app-header">
    <h1 class="app-title">🔍 PokéSearch</h1>
</div>
""", unsafe_allow_html=True)