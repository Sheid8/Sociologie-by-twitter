# File: pages/Statistiques_descriptives.py
import streamlit as st
import pandas as pd
import altair as alt

DATA_PATH = 'data/raw.csv'

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH).drop(columns=["Horodateur"])

st.header("🕵️‍♀️ Statistiques Descriptives")

df = load_data()
var = st.selectbox("Variable :", df.columns.tolist())
counts = df[var].value_counts(normalize=True).reset_index()
counts.columns = [var, 'Proportion']

# Tableau
st.table(counts)

# Pie chart
pie = alt.Chart(counts).mark_arc().encode(
    theta='Proportion:Q',
    color=alt.Color(
        f'{var}:N',
        legend=alt.Legend(title=var)         # ← on affiche la légende avec le nom de la variable
    ),
    tooltip=[f'{var}:N', 'Proportion:Q']
)
st.altair_chart(pie, use_container_width=True)


st.sidebar.markdown(
    """
    <div class="sidebar-footer"> Ici on croit en l'open source ❤️ \n

    Retrouvez le code ici :
      <a href="https://github.com/KrrCharles" target="_blank">
        <i class="fab fa-github"></i> View on GitHub
      </a>

      N'hésitez pas à contribuer directement ou à remonter des bugs

      Site réalisé par
      <a href="https://github.com/KrrCharles" target="_blank">
        <i class="fab fa-github"></i> @KrrCharles
      </a>

      Sur la base du projet de
      <a href="https://x.com/eloivar" target="_blank">
        <i class="fab fa-github"></i> @eloivar
      </a>
    </div>
    """,
    unsafe_allow_html=True,
)