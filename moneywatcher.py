import streamlit as st
import pandas as pd
import plotly.express as px
from database import laad_data

st.set_page_config(page_title="Moneywatcher", layout="wide")

# ==========================================
# 1. DATA INLADEN & FUNCTIES
# ==========================================
laad_data()

def bereken_totaal(lijst, kolomnaam):
    return sum([float(item.get(kolomnaam, 0) or 0) for item in lijst])

# ==========================================
# 2. HET MENU & MAAND KIEZER
# ==========================================
st.sidebar.title("Mijn Systeem ⚙️")

import datetime

maanden_lijst = ["Augustus 2026", "September 2026", "Oktober 2026", "November 2026", "December 2026", "Januari 2027", "Februari 2027"]

# 1. Kijk welke maand het nu ECHT is in de wereld
nu = datetime.datetime.now()
maanden_nl = {1: "Januari", 2: "Februari", 3: "Maart", 4: "April", 5: "Mei", 6: "Juni", 7: "Juli", 8: "Augustus", 9: "September", 10: "Oktober", 11: "November", 12: "December"}
echte_huidige_maand = f"{maanden_nl[nu.month]} {nu.year}"

# 2. Check of deze maand in jouw lijstje staat, anders pakken we de eerste
standaard_maand = echte_huidige_maand if echte_huidige_maand in maanden_lijst else maanden_lijst[0]

# 3. Pak wat je eerder koos in de app, of anders de standaard maand
eerder_gekozen = st.session_state.get('huidige_maand', standaard_maand)

geselecteerde_maand = st.sidebar.selectbox(
    "🗓️ Welke maand wil je bekijken?", 
    maanden_lijst,
    index=maanden_lijst.index(eerder_gekozen) if eerder_gekozen in maanden_lijst else 0
)
st.session_state.huidige_maand = geselecteerde_maand

st.sidebar.divider()
st.sidebar.info("Tip: Vaste kosten en schulden worden automatisch meegerekend in elke maand!")

# ==========================================
# 3. BEREKENINGEN VOOR DE MAAND
# ==========================================
inkomsten_deze_maand = [ink for ink in st.session_state.inkomsten if ink.get("Maand") == geselecteerde_maand]
leefgeld_deze_maand = [lg for lg in st.session_state.leefgeld if lg.get("Maand") == geselecteerde_maand]
facturen_deze_maand = [f for f in st.session_state.variabele_facturen if f.get("Maand") == geselecteerde_maand] # NIEUW

tot_ink = bereken_totaal(inkomsten_deze_maand, 'Bedrag')
tot_leefgeld = bereken_totaal(leefgeld_deze_maand, 'Bedrag')
tot_facturen = bereken_totaal(facturen_deze_maand, 'Bedrag') # NIEUW
tot_vast = bereken_totaal(st.session_state.vaste_kosten, 'Bedrag')
tot_per_maand = bereken_totaal(st.session_state.periodieke_kosten, 'Per Maand Sparen')
tot_schuld_maand = bereken_totaal(st.session_state.schulden, 'Aflossing/mnd')

# Facturen zijn nu ook toegevoegd aan je totale uitgaven!
totale_uitgaven = tot_vast + tot_per_maand + tot_schuld_maand + tot_leefgeld + tot_facturen
reserve = tot_ink - totale_uitgaven

# ==========================================
# 4. HET VISUELE DASHBOARD
# ==========================================
st.title(f"📊 Dashboard: {geselecteerde_maand.upper()}")

# --- RIJ 1: KPI BLOKKEN ---
st.markdown("### 💰 Financiële Samenvatting")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Totale Inkomsten", f"€ {tot_ink:.2f}")
kpi2.metric("Totale Uitgaven", f"€ {totale_uitgaven:.2f}")

if reserve >= 0:
    kpi3.metric("Netto Reserve (Winst)", f"€ {reserve:.2f}")
else:
    kpi3.metric("Netto Tekort (Verlies)", f"€ {reserve:.2f}")
    
kpi4.metric("Totaal Leefgeld", f"€ {tot_leefgeld:.2f}")

st.divider()

# --- RIJ 2: GRAFIEKEN ---
grafiek_col1, grafiek_col2 = st.columns(2)

with grafiek_col1:
    st.markdown("#### 🍩 Cashflow Overzicht")
    
    # Variabele facturen toegevoegd aan de labels
    labels = ['Vaste Kosten', 'Provisie (Jaarlijks)', 'Schulden', 'Leefgeld', 'Var. Facturen', 'Overig / Reserve']
    weergave_reserve = reserve if reserve > 0 else 0
    waardes = [tot_vast, tot_per_maand, tot_schuld_maand, tot_leefgeld, tot_facturen, weergave_reserve]
    
    fig_donut = px.pie(
        names=labels, 
        values=waardes, 
        hole=0.6,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
    st.plotly_chart(fig_donut, use_container_width=True)

with grafiek_col2:
    st.markdown("#### 📊 Uitgaven Verdeling")
    
    # Variabele facturen toegevoegd aan de staven
    data_staven = pd.DataFrame({
        "Categorie": ["Vaste Kosten", "Provisie", "Schulden", "Leefgeld", "Facturen"],
        "Bedrag (€)": [tot_vast, tot_per_maand, tot_schuld_maand, tot_leefgeld, tot_facturen]
    })
    
    fig_bar = px.bar(
        data_staven, 
        x="Categorie", 
        y="Bedrag (€)", 
        text="Bedrag (€)",
        color="Categorie",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_bar.update_traces(texttemplate='€ %{text:.2f}', textposition='outside')
    fig_bar.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)