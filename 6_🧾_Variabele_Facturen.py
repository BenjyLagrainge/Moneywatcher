import streamlit as st
import pandas as pd
from database import laad_data, sla_data_op

laad_data()

# Maand-kiezer
maanden_lijst = ["Augustus 2026", "September 2026", "Oktober 2026", "November 2026", "December 2026", "Januari 2027", "Februari 2027"]
eerder_gekozen = st.session_state.get('huidige_maand', maanden_lijst[0])
huidige_maand = st.sidebar.selectbox("🗓️ Welke maand?", maanden_lijst, index=maanden_lijst.index(eerder_gekozen) if eerder_gekozen in maanden_lijst else 0)
st.session_state.huidige_maand = huidige_maand

st.title(f"🧾 Variabele Facturen ({huidige_maand})")

with st.form("factuur_form"):
    naam = st.text_input("Omschrijving (bijv. Dokter, Water, Boete)")
    bedrag = st.number_input("Bedrag (€)", min_value=0.0, step=10.0)
    if st.form_submit_button("Voeg toe"):
        st.session_state.variabele_facturen.append({
            "Maand": huidige_maand, 
            "Omschrijving": naam, 
            "Bedrag": bedrag
        })
        sla_data_op()
        st.success(f"Factuur toegevoegd aan {huidige_maand}!")
        st.rerun()

andere_maanden = [f for f in st.session_state.variabele_facturen if f.get("Maand") != huidige_maand]
deze_maand = [f for f in st.session_state.variabele_facturen if f.get("Maand") == huidige_maand]

if deze_maand:
    st.write(f"### Facturen in {huidige_maand}")
    df = pd.DataFrame(deze_maand)
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    nieuwe_facturen = andere_maanden + edited_df.to_dict('records')
    if st.session_state.variabele_facturen != nieuwe_facturen:
        st.session_state.variabele_facturen = nieuwe_facturen
        sla_data_op()