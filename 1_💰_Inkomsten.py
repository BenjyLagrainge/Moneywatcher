import streamlit as st
import pandas as pd
import datetime
from database import laad_data, sla_data_op

# Altijd eerst data inladen voor de zekerheid
laad_data()

# ==========================================
# DE SLIMME MAAND-KIEZER (In de zijbalk)
# ==========================================
maanden_lijst = ["Augustus 2026", "September 2026", "Oktober 2026", "November 2026", "December 2026", "Januari 2027", "Februari 2027"]

# Kijk welke maand het nu ECHT is
nu = datetime.datetime.now()
maanden_nl = {1: "Januari", 2: "Februari", 3: "Maart", 4: "April", 5: "Mei", 6: "Juni", 7: "Juli", 8: "Augustus", 9: "September", 10: "Oktober", 11: "November", 12: "December"}
echte_huidige_maand = f"{maanden_nl[nu.month]} {nu.year}"
standaard_maand = echte_huidige_maand if echte_huidige_maand in maanden_lijst else maanden_lijst[0]

# Pak wat je eerder koos, of anders de huidige maand in de echte wereld
eerder_gekozen = st.session_state.get('huidige_maand', standaard_maand)

huidige_maand = st.sidebar.selectbox(
    "🗓️ Welke maand wil je invullen?", 
    maanden_lijst,
    index=maanden_lijst.index(eerder_gekozen) if eerder_gekozen in maanden_lijst else 0
)
st.session_state.huidige_maand = huidige_maand

# ==========================================
# PAGINA LOGICA
# ==========================================
st.title(f"💰 Inkomsten ({huidige_maand})")

with st.form("ink_form"):
    st.write("Voeg een bedrag toe aan je budget:")
    
    # Een handige schakelaar voor het soort inkomst!
    soort = st.radio("Wat wil je toevoegen?", ["Normale inkomst (Loon, etc.)", "Overschot vorige maand"])
    
    # Als je overschot kiest, vult hij de naam automatisch voor je in
    if soort == "Normale inkomst (Loon, etc.)":
        naam = st.text_input("Bron (bijv. Loon, Vakantiegeld)")
    else:
        naam = "Overschot vorige maand"
        
    bedrag = st.number_input("Bedrag (€)", min_value=0.0, step=10.0)
    
    if st.form_submit_button("Voeg toe"):
        st.session_state.inkomsten.append({
            "Maand": huidige_maand, 
            "Bron": naam, 
            "Bedrag": bedrag
        })
        sla_data_op()
        st.success(f"Toegevoegd aan {huidige_maand}!")
        st.rerun()

andere_maanden = [ink for ink in st.session_state.inkomsten if ink.get("Maand") != huidige_maand]
deze_maand = [ink for ink in st.session_state.inkomsten if ink.get("Maand") == huidige_maand]

if deze_maand:
    st.write(f"### Je Inkomstenlijst voor {huidige_maand} (Bewerkbaar)")
    df = pd.DataFrame(deze_maand)
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="edit_ink")
    
    nieuwe_inkomsten = andere_maanden + edited_df.to_dict('records')
    
    # HIER IS DE AANGEPASTE TOAST CODE VOOR INKOMSTEN:
    if st.session_state.inkomsten != nieuwe_inkomsten:
        st.session_state.inkomsten = nieuwe_inkomsten
        sla_data_op()
        st.toast("✅ Inkomsten opgeslagen in de cloud!")
else:
    st.info(f"Je hebt nog geen inkomsten ingevuld voor {huidige_maand}.")