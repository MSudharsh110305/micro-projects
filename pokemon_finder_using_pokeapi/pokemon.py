import streamlit as st
import requests
from typing import List, Dict, Optional, Tuple

st.set_page_config(page_title =" Pokemon Finder", page_icon="✨", layout= "wide")

BASE_URL = "https://pokeapi.co/api/v2"
POKEMON_LIST_LIMIT = 1000
REQUEST_TIMEOUT = 15
