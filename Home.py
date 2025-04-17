import streamlit as st

st.set_page_config(
    page_title="Sociologie by Twitter",
    page_icon="📊",
    layout="wide"
)

st.title("Sociologie by Twitter")
st.markdown(
    """
    **Projet initial de @eloivar sur Twitter :**

    Tout est parti d’un **Google Form** composé de questions volontairement sans rapport  
    L'enquête a obtenu **12 111 réponses** en quelques jours.

    [Voir la vidéo récap](https://www.youtube.com/watch?v=hv8fHrxatjs)

    **Objectifs:**
    - Mettre à l’épreuve un grand échantillon non représentatif  
      (disclaimer : pas de conclusions généralisables !).
    - Découvrir des **corrélations inattendues** entre deux questions sans lien apparent.
    - Tester leur **significativité** (χ² et intervalles de confiance).
    - Explorer l’intégralité du questionnaire en **ACM** et **clustering**.

    Les données sont déjà préchargées : sélectionnez simplement votre analyse  
    dans la barre latérale à gauche et plongez dans ces **résultats funs et scientifiques** !
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