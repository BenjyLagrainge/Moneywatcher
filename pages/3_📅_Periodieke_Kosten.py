import streamlit as st
import pandas as pd

st.title("📅 Jaarlijkse Kosten (Provisie)")
st.write("Vul het JAARbedrag in. De app berekent automatisch hoeveel je per maand aan de kant moet zetten.")

with st.form("per_form"):
    naam = st.text_input("Naam (bijv. Brandverzekering)")
    jaarbedrag = st.number_input("Totaal bedrag per jaar (€)", min_value=0.0, step=10.0)
    if st.form_submit_button("Voeg toe"):
        st.session_state.periodieke_kosten.append({
            "Kostenpost": naam, 
            "Jaarbedrag": jaarbedrag, 
            "Per Maand Sparen": round(jaarbedrag / 12, 2)
        })
        st.success("Toegevoegd!")
        
if st.session_state.periodieke_kosten:
    st.write("### Je Periodieke Kosten (Bewerkbaar)")
    df = pd.DataFrame(st.session_state.periodieke_kosten)
    # We maken de kolom "Per Maand Sparen" dicht (disabled), want die berekent hij zelf
    edited_df = st.data_editor(df, num_rows="dynamic", disabled=["Per Maand Sparen"], use_container_width=True, key="edit_per")
    
    # Automatisch de berekening updaten als je het jaarbedrag aanpast
    edited_df["Per Maand Sparen"] = round(pd.to_numeric(edited_df["Jaarbedrag"], errors='coerce') / 12, 2)
    st.session_state.periodieke_kosten = edited_df.to_dict('records')