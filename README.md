# Sociologie by Twitter

**Projet Streamlit pour explorer une grande enquête Twitter**

Ce dépôt contient une application Streamlit interactive permettant d'analyser les 12 111 réponses d'un Google Form lancé sur Twitter par @eloivar. L'objectif est de découvrir des corrélations inattendues, de tester leur significativité et d'explorer l'ensemble des questions via des analyses descriptives, tris croisés, tests statistiques, ACM et clustering.

---

## 📂 Structure du projet

```
krrcharles-sociologie-by-twitter/
├── Home.py                  # Page d'accueil et configuration Streamlit
├── requirements.txt         # Dépendances Python
├── data/                    # Données brutes (raw.csv à placer ici)
└── pages/                   # Pages Streamlit pour chaque type d'analyse
    ├── 1 - Statistiques_descriptives.py  # Analyse univariée et graphiques circulaires
    ├── 2 - Tris_croises.py               # Tris croisés bivariés et visualisations avancées
    ├── 3 - Tests_statistiques.py         # Tests χ² et intervalles de confiance
    └── 4 - ACM_clustering.py             # Analyse en composantes multiples et clustering
```

---

## ⚙️ Prérequis

- Python 3.8 ou supérieur
- Un terminal (Windows, macOS, Linux)

---

## 🚀 Installation

1. **Cloner** ce dépôt :
   ```bash
   git clone https://github.com/KrrCharles/krrcharles-sociologie-by-twitter.git
   cd krrcharles-sociologie-by-twitter
   ```

2. **Créer et activer** un environnement virtuel (optionnel mais recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Installer** les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. **Ajouter** le fichier de données brutes `raw.csv` dans le dossier `data/`.

---

## 💻 Lancer l'application

Dans le répertoire du projet, exécutez :
```bash
streamlit run Home.py
```

Puis ouvrez l'URL indiquée (généralement `http://localhost:8501`) dans votre navigateur.

---

## 📊 Pages et analyses

1. **Statistiques descriptives** (`pages/1 - Statistiques_descriptives.py`) : univariées, proportion et camembert interactif.
2. **Tris croisés** (`pages/2 - Tris_croises.py`) : tables de contingence, mosaic plot, barres empilées, balloon plot, parallel sets, divergent bar.
3. **Tests statistiques** (`pages/3 - Tests_statistiques.py`) : calcul de χ², p-value et intervalles de confiance par bootstrap.
4. **ACM & clustering** (`pages/4 - ACM_clustering.py`) : projection en composantes multiples et segmentation par k-means.

---

## 🤝 Contribuer

Contributions, suggestions et rapports de bugs sont les bienvenus ! :heart:

1. Forkez ce dépôt
2. Créez une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commitez vos modifications (`git commit -m "Ajout ..."`)
4. Pushez (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une Pull Request

---

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

