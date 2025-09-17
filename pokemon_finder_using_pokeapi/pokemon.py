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
def get_sprite_url(pokemon_data):
    sprites = pokemon_data.get("sprites", {})
    other = sprites.get("other", {})
    

st.markdown("""
<div class="app-header">
    <h1 class="app-title">🔍 PokéSearch</h1>
</div>
""", unsafe_allow_html=True)

pokemon_name = st.text_input("", placeholder="Enter Pokémon name or ID", key="search", label_visibility="collapsed")

search_button = st.button("Search")

if (search_button and pokemon_name) and pokemon_name.strip():
    with st.empty():
        st.markdown('<div class="loading">🔍 Searching...</div>', unsafe_allow_html=True)

        pokemon_data = fetch_pokemon_data(pokemon_name.strip())
        if pokemon_data:
            st.empty()
            st.markdown('<div class = "pokemon-card">', unsafe_allow_html=True)

            name = pokemon_data["name"].capitalize()
            poke_id = pokemon_data["id"]
            types = [t["type"]["name"] for t in pokemon_data["types"]]
            st.markdown(f'<h2 class="pokemon-name">{name}</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="pokemon-id">#{poke_id:03d}</div>', unsafe_allow_html=True)
            st.markdown('<div class="pokemon-types">{ }</div>'.format(' '.join(
                f'<span class="type-badge" style="background-color: {TYPE_COLORS.get(t, "#68A090")};">{t.capitalize()}</span>' for t in types)), unsafe_allow_html=True)
            
            sprite_url = get_sprite_url(pokemon_data)
            if sprite_url:
                st.markdown('<div class="pokemon-image">', unsafe_allow_html=True)
                st.image(sprite_url, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)                
            height_m = pokemon_data.get("height", 0) / 10
            weight_kg = pokemon_data.get("weight", 0) / 10
            base_exp = pokemon_data.get("base_experience", "N/A")
            st.markdown(f'''
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Height</div>
                    <div class="info-value">{height_m:.1f}m</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Weight</div>
                    <div class="info-value">{weight_kg:.1f}kg</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Base XP</div>
                    <div class="info-value">{base_exp}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">ID</div>
                    <div class="info-value">#{poke_id}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            abilities = [a["ability"]["name"] for a in pokemon_data.get("abilities", [])]
            if abilities:
                abilities_html = "".join([f'<span class="ability-item">{a.replace("-", " ")}</span>' for a in abilities])
                st.markdown(f'''
                <div class="abilities">
                    <div class="abilities-title">Abilities</div>
                    {abilities_html}
                </div>
                ''', unsafe_allow_html=True)
            
            stats = pokemon_data.get("stats", [])
            if stats:
                st.markdown('<div class="stats-section">', unsafe_allow_html=True)
                st.markdown('<div class="stats-title">📊 Base Stats</div>', unsafe_allow_html=True)
                
                for stat in stats:
                    stat_name = stat["stat"]["name"].replace("-", " ")
                    stat_value = stat["base_stat"]
                    progress_width = min((stat_value / 200) * 100, 100)
                    
                    st.markdown(f'''
                    <div class="stat-row">
                        <div class="stat-name">{stat_name}</div>
                        <div class="stat-bar-container">
                            <div class="stat-bar" style="width: {progress_width}%"></div>
                        </div>
                        <div class="stat-value">{stat_value}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.markdown(f'''
            <div class="error-card">
                <strong>Pokémon not found!</strong><br>
                <small>Try "{pokemon_name}" with correct spelling or use ID (1-1010)</small>
            </div>
            ''', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; color: #6c757d;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📱</div>
        <div style="font-size: 1.1rem; font-weight: 500; margin-bottom: 0.5rem;">Search any Pokémon</div>
        <div style="font-size: 0.9rem;">Try "pikachu", "charizard", or "25"</div>
    </div>
    """, unsafe_allow_html=True)