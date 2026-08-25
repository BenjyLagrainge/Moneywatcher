import json
import os
import streamlit as st

# De naam van het onzichtbare bestandje op je Mac
BESTAND = "mijn_budget_data.json"

def laad_data():
    """Haalt de data uit het bestand en zet het in het geheugen van de app."""
    standaard_data = {
        "inkomsten": [],
        "vaste_kosten": [],
        "periodieke_kosten": [],
        "schulden": [],
        "leefgeld": []
    }
    
    # Als het bestand al bestaat, lees het dan uit
    if os.path.exists(BESTAND):
        with open(BESTAND, "r") as file:
            try:
                opgeslagen_data = json.load(file)
                standaard_data.update(opgeslagen_data)
            except:
                pass # Als het bestand leeg of stuk is, gebeurt er niets
                
    # Stop alles veilig in de ladekasten (session_state)
    for lade, inhoud in standaard_data.items():
        if lade not in st.session_state:
            st.session_state[lade] = inhoud

def sla_data_op():
    """Pakt het huidige geheugen en schrijft het definitief weg naar het bestand."""
    data_om_te_bewaren = {
        "inkomsten": st.session_state.get("inkomsten", []),
        "vaste_kosten": st.session_state.get("vaste_kosten", []),
        "periodieke_kosten": st.session_state.get("periodieke_kosten", []),
        "schulden": st.session_state.get("schulden", []),
        "leefgeld": st.session_state.get("leefgeld", [])
    }
    
    with open(BESTAND, "w") as file:
        json.dump(data_om_te_bewaren, file, indent=4)