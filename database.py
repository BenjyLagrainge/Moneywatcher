import streamlit as st
import requests

# We gebruiken hier de NAAM van je secret, Streamlit Cloud doet de rest!
BIN_ID = st.secrets["BIN_ID"]
API_KEY = st.secrets["API_KEY"]
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

# We voegen 'X-Bin-Versioning': 'false' toe zodat hij je kluis direct overschrijft zonder verwarrende 'versies' aan te maken.
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json",
    "X-Bin-Versioning": "false" 
}

def laad_data():
    """Haalt data uit de kluis (1x per sessie om blokkades te voorkomen)."""
    if "data_geladen" in st.session_state:
        return # We hebben de data al, we hoeven het internet niet opnieuw op!
        
    standaard_data = {
        "inkomsten": [],
        "vaste_kosten": [],
        "periodieke_kosten": [],
        "schulden": [],
        "leefgeld": [],
        "variabele_facturen": []
    }
    
    try:
        response = requests.get(URL, headers=HEADERS)
        if response.status_code == 200:
            opgeslagen_data = response.json().get("record", {})
            standaard_data.update(opgeslagen_data)
        else:
            st.error(f"Fout bij ophalen! Code: {response.status_code}")
    except Exception as e:
        pass 
            
    for lade, inhoud in standaard_data.items():
        st.session_state[lade] = inhoud
        
    # Markeer dat we klaar zijn met laden
    st.session_state["data_geladen"] = True

def sla_data_op():
    """Schrijft de nieuwe data direct weg en toont een pop-up."""
    data_om_te_bewaren = {
        "inkomsten": st.session_state.get("inkomsten", []),
        "vaste_kosten": st.session_state.get("vaste_kosten", []),
        "periodieke_kosten": st.session_state.get("periodieke_kosten", []),
        "schulden": st.session_state.get("schulden", []),
        "leefgeld": st.session_state.get("leefgeld", []),
        "variabele_facturen": st.session_state.get("variabele_facturen", [])
    }
    
    try:
        response = requests.put(URL, json=data_om_te_bewaren, headers=HEADERS)
        if response.status_code == 200:
            st.toast("✅ Veilig opgeslagen in de cloud!")
        else:
            st.error(f"Fout bij opslaan! (Code {response.status_code})")
    except Exception as e:
        st.error(f"Geen verbinding met internet: {e}")