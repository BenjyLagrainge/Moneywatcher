import streamlit as st
import pandas as pd

huidige_maand = st.session_state.get('huidige_maand', 'Augustus 2026')

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
        st.success(f"Budget toegevoegd voor {huidige_maand}!")
        st.rerun()
        
andere_maanden = [lg for lg in st.session_state.leefgeld if lg.get("Maand") != huidige_maand]
deze_maand = [lg for lg in st.session_state.leefgeld if lg.get("Maand") == huidige_maand]

if deze_maand:
    st.write(f"### Je Budgetten voor {huidige_maand} (Bewerkbaar)")
    df = pd.DataFrame(deze_maand)
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="edit_leefgeld")
    
    st.session_state.leefgeld = andere_maanden + edited_df.to_dict('records')
else:
    st.info(f"Je hebt nog geen leefgeld-budgetten ingevuld voor {huidige_maand}.")