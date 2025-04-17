import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np
from prince import MCA
from sklearn.cluster import KMeans

DATA_PATH = 'data/raw.csv'

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH).drop(columns=["Horodateur"])

st.header("🤞 Tris Croisés Bivariés")

# Chargement
df = load_data()
cols = df.columns.tolist()
# 1) Définissez le callback qui échange les valeurs
def swap_vars():
    st.session_state.x, st.session_state.y = st.session_state.y, st.session_state.x

# 2) Créez le bouton AVANT les selectbox, en lui passant ce callback
st.button("↔️ Inverser X et Y", on_click=swap_vars, key="swap_btn")

# 3) Maintenant seulement, on instancie les widgets liés à session_state.x et .y
cols = df.columns.tolist()
var1 = st.selectbox("Variable X :", cols, key='x')
cols_y = [c for c in cols if c != var1]
var2 = st.selectbox("Variable Y :", cols_y, key='y')

# Table de contingence
ctab = pd.crosstab(df[var1], df[var2], normalize='index')
st.subheader("Table de contingence")
st.dataframe(ctab)

# Calcul des proportions globales de la population
global_props = df[var2].value_counts(normalize=True)

# Choix du type de viz
viz = st.selectbox(
    "Type de visualisation :",
    [
        "Mosaic Plot",
        "Segmented Bar Chart",
        "Balloon Plot",
        "Parallel Sets",
        "Divergent Bar"
    ]
)


# 1. Mosaic Plot (Treemap)
if viz == "Mosaic Plot":
    st.subheader("Mosaic Plot (Treemap) avec écart à la population générale")
    # Calculer proportions conditionnelles et différences
    ct = pd.crosstab(df[var1], df[var2], normalize='index')
    df_ct = ct.reset_index().melt(id_vars=[var1], var_name=var2, value_name='prop')
    df_ct['global'] = df_ct[var2].map(global_props)
    df_ct['diff'] = df_ct['prop'] - df_ct['global']
    # Treemap : taille = prop (count implicite) ; couleur = diff
    fig = px.treemap(
        df_ct,
        path=[var1, var2],
        values='prop',
        color='diff',
        color_continuous_midpoint=0,
        labels={'prop': 'Prop. cond.', 'diff': 'Écart à global'}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    ### Comment lire ce graphique :

    🚨 Attention aux échelles, parfois très faibles, des grandes différences apparaissent peut être pour une différence réelle faible

    Structure : chaque rectangle représente la combinaison d’une modalité de X (axe principal) et d’une modalité de Y (feuillet).

    Taille : proportion conditionnelle de Y au sein de chaque modalité de X (plus le rectangle est grand, plus cette combinaison est fréquente).

    Couleur : écart à la proportion globale de la modalité de Y ; les teintes chaudes (positives) signent une surreprésentation, les teintes froides (négatives) une sous-représentation.

    Lecture : repérer les gros rectangles pour savoir quelles associations dominent, et leur coloration pour voir si elles sont proportionnellement plus ou moins fréquentes que dans l’ensemble de la population."""
    )
# 2. Segmented Bar Chart
elif viz == "Segmented Bar Chart":
    st.subheader("Segmented Bar Chart avec barre de population générale")
    ctab = pd.crosstab(df[var1], df[var2], normalize='index')
    # Ajouter une ligne pour la population générale
    ctab.loc['Population générale'] = global_props
    df_bar = ctab.reset_index().melt(id_vars=[var1], var_name=var2, value_name='proportion')
    fig = px.bar(
        df_bar,
        x=var1,
        y='proportion',
        color=var2,
        barmode='stack',
        labels={'proportion':'Proportion'}
    )
    fig.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    ### Comment lire ce graphique :

    🚨 Attention aux échelles, parfois très faibles, des grandes différences apparaissent peut être pour une différence réelle faible

    Structure : pour chaque modalité de X, une barre empilée décompose la répartition de Y.

    Hauteur totale : 100 % (proportions conditionnelles normalisées).

    Lecture :

    Comparez la composition interne de chaque barre X avec celle de la barre générale.

    Repérez si certaines catégories de Y sont surreprésentées dans un groupe X (segments plus larges que dans la barre générale).
    """
    )

# 3. Balloon Plot
elif viz == "Balloon Plot":
    st.subheader("Balloon Plot avec série de ballons pour population générale")
    # Proportions conditionnelles
    ct = pd.crosstab(df[var1], df[var2], normalize='index')
    # Ajouter une ligne pour la population générale
    ct.loc['Population générale'] = global_props
    heat = ct.reset_index().melt(id_vars=[var1], var_name=var2, value_name='p')
    # Scatter : taille = proportion, série distincte pour chaque niveau de var1 (dont population générale)
    fig = px.scatter(
        heat,
        x=var2,
        y=var1,
        size='p',
        size_max=50,
        labels={'p': 'Proportion'}
    )
    fig.update_traces(marker=dict(opacity=0.7))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    ### Comment lire ce graphique :
    
    🚨 Attention aux échelles, parfois très faibles, des grandes différences apparaissent peut être pour une différence réelle faible

    Structure : un nuage de points disposé en grille, axes X = modalités de Y, axes Y = modalités de X (dont « Population générale »).

    Taille des bulles : proportion de Y dans chaque modalité de X.

    Séries distinctes : une rangée de bulles représente toujours la population générale ou une modalité de X donnée.

    Lecture :

    Comparez facilement les bulles d’une même colonne (modalité Y) pour voir où la proportion est la plus forte.

    Repérez la bulle de la population générale comme référence visuelle (si elle apparaît plus grande ou plus petite que les autres).

    Des bulles très petites signalent des associations rares, des bulles très grandes des associations fréquentes.
    """
    )

# 6. Parallel Sets
elif viz == "Parallel Sets":
    st.subheader("Parallel Sets (Parallel Categories)")
    fig = px.parallel_categories(
    df,
    dimensions=[var1, var2]
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    ### Comment lire ce graphique :
    
    🚨 Attention aux échelles, parfois très faibles, des grandes différences apparaissent peut être pour une différence réelle faible

    Structure : deux axes verticaux représentant X et Y, reliés par des flux (cordes).

    Épaisseur des flux : proportion conditionnelle de chaque modalité Y au sein de chaque modalité X.

    Couleur (optionnelle) : écart à la proportion globale (le gradient accentue les flux sur‑ ou sous‑représentés).

    Lecture :

    Suivez visuellement l’épaisseur des cordes de X vers Y pour comprendre les transitions.

    Les connexions épaisses pointent les associations majeures.

    La comparaison des couleurs ou largeurs permet de détecter les biais par rapport à la distribution globale.
        """
    )


# 8. Divergent Bar
elif viz == "Divergent Bar":
    st.subheader("Divergent Bar")
    mod2 = st.selectbox(f"Modalité de {var2} :", df[var2].unique())
    cond = df.groupby(var1).apply(lambda g: (g[var2] == mod2).mean())
    overall = (df[var2] == mod2).mean()
    diff = (cond - overall).reset_index(name='diff')
    fig = px.bar(
        diff, x='diff', y=var1, orientation='h',
        color='diff', color_continuous_midpoint=0,
        labels={'diff': 'Écart à global'}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    ### Comment lire ce graphique :

    🚨 Attention aux échelles, parfois très faibles, des grandes différences apparaissent peut être pour une différence réelle faible

    Structure : pour une modalité choisie de Y, barre horizontale pour chaque modalité de X représentant l’écart (positif ou négatif) à la proportion globale.

    Lecture :

    Identifiez très vite les groupes X où la modalité Y est surreprésentée (barres positives les plus longues).

    Inversement, repérez les sous‑représentations (barres négatives).
        """
    )


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