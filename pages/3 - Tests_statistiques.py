import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

DATA_PATH = 'data/raw.csv'

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_data
def compute_bootstrap_ci(series, n_boot=1000, ci=95):
    boot_props = [series.sample(len(series), replace=True).mean() for _ in range(n_boot)]
    return series.mean(), np.percentile(boot_props, (100-ci)/2), np.percentile(boot_props, 100-(100-ci)/2)

st.header("3️⃣ Tests Statistiques (χ² & IC) (WIP)")

df = load_data().drop(columns=["Horodateur"])
var1 = st.selectbox("Variable A :", df.columns.tolist(), key='A')
var2 = st.selectbox("Variable B :", df.columns.tolist(), key='B')
modal1 = st.selectbox(f"Modalité de {var1} :", df[var1].unique(), key='m1')
modal2 = st.selectbox(f"Modalité de {var2} :", df[var2].unique(), key='m2')
sub = df[df[var1] == modal1]
series = (sub[var2] == modal2).astype(int)
prop, low, high = compute_bootstrap_ci(series)
chi2, p, _, _ = stats.chi2_contingency(pd.crosstab(df[var1], df[var2]))
st.write(f"Proportion : {prop:.3f}")
st.write(f"IC95 % : [{low:.3f}, {high:.3f}]")
st.write(f"χ² = {chi2:.3f}, p-value = {p:.3f}")


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