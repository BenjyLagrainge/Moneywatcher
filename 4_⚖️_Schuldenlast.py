import streamlit as st
import pandas as pd
import datetime
from database import sla_data_op # <--- BELANGRIJK: Deze is toegevoegd!

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
        sla_data_op() # Meteen opslaan in de cloud!
        st.success("Schuld geregistreerd!")
        
# 2. De data bewerken en tonen
if st.session_state.schulden:
    
    # ==========================================
    # HIER KOMT DE NIEUWE AFSCHRIJF-KNOP
    # ==========================================
    st.write("### 📉 Maandelijkse Afschrijving")
    st.info("Klik één keer per maand op deze knop om de aflossing van je openstaande bedragen af te trekken.")

    if st.button("💸 Trek aflossingen af (Voor deze maand)"):
        nieuwe_schulden_lijst = []
        
        for schuld in st.session_state.schulden:
            # Aangepast naar jouw kolomnaam: "Bedrag (€)"
            huidig_bedrag = float(schuld.get("Bedrag (€)", 0))
            aflossing = float(schuld.get("Aflossing/mnd", 0))
            
            nieuw_bedrag = max(0.0, huidig_bedrag - aflossing)
            
            schuld["Bedrag (€)"] = nieuw_bedrag
            nieuwe_schulden_lijst.append(schuld)
            
        st.session_state.schulden = nieuwe_schulden_lijst
        sla_data_op() # Sla de nieuwe lagere saldo's op in de cloud
        st.success("BAM! Alle aflossingen zijn van het openstaande bedrag afgetrokken.")
        st.rerun()
    # ==========================================
    
    st.write("### Beheer je Schulden (Pas saldo of aflossing aan)")
    df_base = pd.DataFrame(st.session_state.schulden)
    edited_base = st.data_editor(df_base, num_rows="dynamic", use_container_width=True, key="edit_schulden")
    
    # Check of er iets handmatig is veranderd in de tabel en sla dit op
    if st.session_state.schulden != edited_base.to_dict('records'):
        st.session_state.schulden = edited_base.to_dict('records')
        sla_data_op()
    
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