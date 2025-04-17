# File: pages/ACM_clustering.py
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import prince
import plotly.express as px

DATA_PATH = 'data/raw.csv'

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH).astype(str)

st.header("4️⃣ ACM & Clustering (WIP)")

df = load_data().drop(columns=["Horodateur"])

# ACM
mca = prince.MCA(n_components=2, random_state=42)
coords = mca.fit_transform(df)
fig = px.scatter(coords, x=0, y=1, title="Projection ACM")

# Ajout du quadrillage
fig.update_layout(
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)
st.plotly_chart(fig, use_container_width=True)

# Clustering
k = st.slider("Nombre de clusters", 2, 6, 3)
km = KMeans(n_clusters=k, random_state=42).fit(coords)
coords['cluster'] = km.labels_.astype(str)
fig2 = px.scatter(coords, x=0, y=1, color='cluster', title="Clusters ACM")

# Quadrillage aussi sur le clustering
fig2.update_layout(
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)
st.plotly_chart(fig2, use_container_width=True)

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
