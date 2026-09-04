import streamlit as st
import pandas as pd
import datetime  # <--- Nodig voor de slimme klok
from database import laad_data, sla_data_op

# 1. Altijd eerst je data inladen uit de kluis!
laad_data()

# ==========================================
# DE SLIMME MAAND-KIEZER (In de zijbalk)
# ==========================================
maanden_lijst = ["Augustus 2026", "September 2026", "Oktober 2026", "November 2026", "December 2026", "Januari 2027", "Februari 2027"]

nu = datetime.datetime.now()
maanden_nl = {1: "Januari", 2: "Februari", 3: "Maart", 4: "April", 5: "Mei", 6: "Juni", 7: "Juli", 8: "Augustus", 9: "September", 10: "Oktober", 11: "November", 12: "December"}
echte_huidige_maand = f"{maanden_nl[nu.month]} {nu.year}"
standaard_maand = echte_huidige_maand if echte_huidige_maand in maanden_lijst else maanden_lijst[0]

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
st.title(f"🛒 Leefgeld ({huidige_maand})")
st.write(f"Beheer hier je budgetten (boodschappen, tanken, ontspanning) voor **{huidige_maand}**.")

with st.form("leefgeld_form"):
    naam = st.text_input("Categorie (bijv. Boodschappen Colruyt)")
    bedrag = st.number_input("Bedrag (€)", min_value=0.0, step=10.0)
    if st.form_submit_button("Voeg toe aan budget"):
        st.session_state.leefgeld.append({
            "Maand": huidige_maand, 
            "Categorie": naam, 
            "Bedrag": bedrag
        })
        sla_data_op()
        st.success(f"Budget toegevoegd voor {huidige_maand}!")
        st.rerun()
        
andere_maanden = [lg for lg in st.session_state.leefgeld if lg.get("Maand") != huidige_maand]
deze_maand = [lg for lg in st.session_state.leefgeld if lg.get("Maand") == huidige_maand]

if deze_maand:
    st.write(f"### Je Budgetten voor {huidige_maand} (Bewerkbaar)")
    df = pd.DataFrame(deze_maand)
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="edit_leefgeld")
    
    nieuwe_leefgeld_lijst = andere_maanden + edited_df.to_dict('records')
    
    # Check of er iets handmatig is veranderd in de tabel. Zo ja? Opslaan!
    if st.session_state.leefgeld != nieuwe_leefgeld_lijst:
        st.session_state.leefgeld = nieuwe_leefgeld_lijst
        sla_data_op()
        st.toast("✅ Leefgeld opgeslagen in de cloud!") # <--- De handige pop-up!
else:
    st.info(f"Je hebt nog geen leefgeld-budgetten ingevuld voor {huidige_maand}.")