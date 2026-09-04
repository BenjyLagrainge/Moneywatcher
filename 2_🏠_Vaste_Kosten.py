import streamlit as st
import pandas as pd

st.title("🏠 Vaste Maandelijkse Kosten")
st.write("Beheer hier je maandelijkse terugkerende lasten zoals je lening, energie en internet.")

with st.form("vast_form"):
    naam = st.text_input("Naam (bijv. Elektriciteit)")
    bedrag = st.number_input("Bedrag per maand (€)", min_value=0.0, step=10.0)
    if st.form_submit_button("Voeg toe"):
        st.session_state.vaste_kosten.append({"Kostenpost": naam, "Bedrag": bedrag})
        st.success("Toegevoegd!")
        
if st.session_state.vaste_kosten:
    st.write("### Je Vaste Kosten (Bewerkbaar)")
    df = pd.DataFrame(st.session_state.vaste_kosten)
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="edit_vast")
    st.session_state.vaste_kosten = edited_df.to_dict('records')