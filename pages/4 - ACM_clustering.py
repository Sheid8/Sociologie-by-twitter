import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import prince
import plotly.graph_objects as go
import plotly.express as px

DATA_PATH = 'data/raw.csv'

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH).astype(str)

st.header("4️⃣ ACM & Clustering (WIP)")
st.subheader("C'est plus compliqué mais c'est expliqué en dessous et dans la vidéo")

df = load_data().drop(columns=["Horodateur"])

# ACM
mca = prince.MCA(n_components=2, random_state=42)
coords = mca.fit_transform(df)

# Coordonnées des variables
var_coords = mca.column_coordinates(df)
var_coords.columns = [0, 1]
var_coords['variable'] = var_coords.index

# Calcul des inerties expliquées
eigenvalues = mca.eigenvalues_
inertias = eigenvalues / eigenvalues.sum()

# Calcul d'une mesure d'importance (distance à l'origine)
var_coords['distance'] = np.sqrt(var_coords[0]**2 + var_coords[1]**2)
max_dist = float(var_coords['distance'].max())

# Slider pour filtrer les modalités "importantes" avec valeur par défaut
threshold = st.slider(
    "Seuil de distance pour affichage des modalités", 
    min_value=0.0, 
    max_value=round(max_dist, 2), 
    value=0.5,  # valeur par défaut
    step=round(max_dist/100, 2) if max_dist > 0 else 0.1
)

# Filtre des modalités selon le seuil
filtered = var_coords[var_coords['distance'] >= threshold]

# Graphique projection (modalités filtrées)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=filtered[0],
    y=filtered[1],
    mode='markers+text',
    name='Modalités',
    marker=dict(size=8, color='red'),
    text=filtered['variable'],
    textposition='top center',
    hovertemplate='Variable %{text}<br>F1 = %{x:.2f}<br>F2 = %{y:.2f}<br>Distance = %{customdata:.2f}',
    customdata=filtered['distance']
))
fig.update_layout(
    title=f"Projection ACM des modalités (distance ≥ {threshold:.2f})",
    xaxis=dict(title=f"F1 ({inertias[0]*100:.2f}% inertie)", showgrid=True),
    yaxis=dict(title=f"F2 ({inertias[1]*100:.2f}% inertie)", showgrid=True),
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# Paragraphe explicatif pour novices
st.markdown("""
**Comment lire ce graphique ?**  
- Le graphique montre uniquement les modalités (valeurs) des variables qui sont les plus « importantes » dans l’analyse.  
- L’importance est ici mesurée par la **distance** d’un point au centre : plus un point est loin, plus cette modalité aide à expliquer les relations dans vos données.  
- Déplacez le curseur pour ne garder que les modalités avec une distance supérieure au seuil choisi (par défaut 0.5).  
- Cela permet de filtrer les modalités moins influentes et de se concentrer sur celles qui structurent vraiment l’espace factoriel.
""", unsafe_allow_html=True)

# Clustering
k = st.slider("Nombre de clusters", 2, 6, 3)
km = KMeans(n_clusters=k, random_state=42).fit(coords)
coords['cluster'] = km.labels_.astype(str)
fig2 = px.scatter(coords, x=0, y=1, color='cluster', title="Clusters ACM")
fig2.update_layout(
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)
st.plotly_chart(fig2, use_container_width=True)

# Sidebar
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
