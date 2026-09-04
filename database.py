import streamlit as st
import requests
import json  # <--- Extra hulpmiddel om data veilig te verpakken

BIN_ID = st.secrets["BIN_ID"]
API_KEY = st.secrets["API_KEY"]
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

def laad_data():
    """Haalt data uit de kluis (1x per sessie)."""
    if "data_geladen" in st.session_state:
        return 
        
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
    except:
        pass 
            
    for lade, inhoud in standaard_data.items():
        st.session_state[lade] = inhoud
        
    st.session_state["data_geladen"] = True

def sla_data_op():
    """Schrijft de data weg en BEVRIEST de app als het mislukt."""
    data_om_te_bewaren = {
        "inkomsten": st.session_state.get("inkomsten", []),
        "vaste_kosten": st.session_state.get("vaste_kosten", []),
        "periodieke_kosten": st.session_state.get("periodieke_kosten", []),
        "schulden": st.session_state.get("schulden", []),
        "leefgeld": st.session_state.get("leefgeld", []),
        "variabele_facturen": st.session_state.get("variabele_facturen", [])
    }
    
    try:
        # Dit filter zorgt dat Pandas-getallen worden omgezet naar leesbare tekst voor het internet
        veilige_data = json.loads(json.dumps(data_om_te_bewaren, default=str))
        
        response = requests.put(URL, json=veilige_data, headers=HEADERS)
        
        if response.status_code == 200:
            st.toast("✅ Succesvol opgeslagen in de cloud!")
        else:
            # Als JSONBin weigert, tonen we de fout en TREKKEN WE AAN DE NOODREM
            st.error(f"🛑 JSONBIN FOUT! Code: {response.status_code}. Melding: {response.text}")
            st.stop() 
            
    except Exception as e:
        # Als er een interne Python fout is, TREKKEN WE AAN DE NOODREM
        st.error(f"🛑 INTERNE FOUT tijdens opslaan: {e}")
        st.stop()