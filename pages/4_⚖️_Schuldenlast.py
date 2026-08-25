import streamlit as st
import pandas as pd
import datetime

st.title("⚖️ Overzicht Schulden & Aflossingstabel")

# 1. Formulier
with st.form("schuld_form"):
    col1, col2 = st.columns(2)
    with col1:
        schuldeiser = st.text_input("Schuldeiser / Omschrijving (bijv. Intrum)")
        totaal_saldo = st.number_input("Startbedrag (€)", min_value=0.0, step=50.0)
    with col2:
        afbetaling = st.number_input("Aflossing per maand (€)", min_value=0.0, step=10.0)
        
    if st.form_submit_button("Voeg schuld toe"):
        st.session_state.schulden.append({
            "Schuldeiser": schuldeiser,
            "Bedrag (€)": totaal_saldo,
            "Aflossing/mnd": afbetaling
        })
        st.success("Schuld geregistreerd!")
        
# 2. De data bewerken en tonen
if st.session_state.schulden:
    st.write("### Beheer je Schulden (Pas saldo of aflossing aan)")
    df_base = pd.DataFrame(st.session_state.schulden)
    edited_base = st.data_editor(df_base, num_rows="dynamic", use_container_width=True, key="edit_schulden")
    st.session_state.schulden = edited_base.to_dict('records')
    
    st.divider()
    st.subheader("Jouw Aflossingstabel (Komende 6 maanden)")
    
    vandaag = datetime.date.today()
    maand_namen = ["JAN", "FEB", "MRT", "APR", "MEI", "JUN", "JUL", "AUG", "SEP", "OKT", "NOV", "DEC"]
    
    tabel_data = []
    for schuld in st.session_state.schulden:
        bedrag = float(schuld.get("Bedrag (€)", 0) or 0)
        aflossing = float(schuld.get("Aflossing/mnd", 0) or 0)
        
        rij = {
            "Schuldeiser": schuld.get("Schuldeiser", ""),
            "Startbedrag (€)": bedrag,
            "Aflossing/mnd": aflossing
        }
        
        restant = bedrag
        for i in range(1, 7):
            toekomstige_maand_index = (vandaag.month + i - 1) % 12
            toekomstige_maand_naam = maand_namen[toekomstige_maand_index]
            
            restant = max(0, restant - aflossing)
            rij[toekomstige_maand_naam] = round(restant, 2)
            
        tabel_data.append(rij)
        
    st.dataframe(pd.DataFrame(tabel_data), use_container_width=True, hide_index=True)