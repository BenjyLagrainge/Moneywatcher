import streamlit as st
import requests

# Haal de geheime codes op uit de veilige Streamlit-kluis
BIN_ID = st.secrets["BIN_ID"]
API_KEY = st.secrets["API_KEY"]
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

def laad_data():
    """Haalt de data uit de online kluis (JSONBin) in plaats van je Mac."""
    standaard_data = {
        "inkomsten": [],
        "vaste_kosten": [],
        "periodieke_kosten": [],
        "schulden": [],
        "leefgeld": [],
        "variabele_facturen": []  # <--- Hier is je nieuwe ladekast!
    }
    
    try:
        # Vraag de data op bij het internet
        response = requests.get(URL, headers=HEADERS)
        if response.status_code == 200:
            # Als het lukt, overschrijf de standaard_data met jouw online data
            opgeslagen_data = response.json().get("record", {})
            standaard_data.update(opgeslagen_data)
    except:
        # Als er even geen internet is, doen we niets en pakken we lege data
        pass 
            
    # Stop alles veilig in de ladekasten (session_state) van de app
    for lade, inhoud in standaard_data.items():
        if lade not in st.session_state:
            st.session_state[lade] = inhoud

def sla_data_op():
    """Schrijft de nieuwe data direct weg naar de online kluis."""
    data_om_te_bewaren = {
        "inkomsten": st.session_state.get("inkomsten", []),
        "vaste_kosten": st.session_state.get("vaste_kosten", []),
        "periodieke_kosten": st.session_state.get("periodieke_kosten", []),
        "schulden": st.session_state.get("schulden", []),
        "leefgeld": st.session_state.get("leefgeld", []),
        "variabele_facturen": st.session_state.get("variabele_facturen", []) # <--- En hier wordt hij veilig weggeschreven!
    }
    
    try:
        # Stuur het hele pakketje naar JSONBin
        requests.put(URL, json=data_om_te_bewaren, headers=HEADERS)
    except:
        pass