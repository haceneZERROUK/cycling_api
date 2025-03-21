# Projet Cyclisme API 🚴‍♂️💨

Bienvenue dans le projet **Cycling API** ! Cette application a pour objectif de fournir une solution moderne et robuste pour enregistrer et analyser les performances des athlètes cyclistes. Elle est conçue pour les entraîneurs et les gestionnaires d'équipes cyclistes afin d'améliorer l'entraînement, suivre les progrès et évaluer les performances des cyclistes.

## Objectifs du Projet 🎯

L'objectif principal de ce projet est de fournir une API RESTful qui permettra de :
1. **Gérer l'authentification des utilisateurs** – Inscription, connexion et gestion des tokens JWT.
2. **Enregistrer et gérer les performances des athlètes** – Suivi de données essentielles telles que la puissance, le VO2max, la cadence, la fréquence cardiaque et le rapport poids/puissance.
3. **Fournir des statistiques avancées** sur les athlètes, comme l'athlète le plus puissant, celui avec la VO2max la plus élevée et celui avec le meilleur rapport poids/puissance.

### Bonus 🎁
- **Interface Streamlit** pour une expérience interactive permettant aux utilisateurs d'ajouter, modifier, consulter des performances et visualiser des statistiques.
- **Intégration Power BI** pour des analyses et tableaux de bord plus poussés.

## Fonctionnalités de l'API 🚀

### Authentification & Sécurité 🔒
- Inscription des utilisateurs avec un mot de passe sécurisé.
- Connexion via JWT pour une gestion sécurisée des sessions.
- Protection des routes et des fonctionnalités via un mécanisme d'authentification basé sur des tokens.

### Gestion des Athlètes & Performances 💪
- **Ajouter un athlète** : Créez un profil avec des informations comme le nom, l'âge, le poids, la taille, le VO2max, etc.
- **Enregistrer les performances** : Suivez les performances des athlètes (puissance, cadence, fréquence cardiaque, VO2max, etc.) avec des tests réguliers.
- **Modification et suppression** : Les utilisateurs authentifiés peuvent modifier ou supprimer les performances des athlètes.

### Statistiques des Athlètes 📊
- Le système calcule automatiquement l'athlète ayant la **meilleure puissance moyenne**, la **VO2max la plus élevée** et le **meilleur rapport poids/puissance**.

## Interface avec Streamlit 📈
Nous avons ajouté une interface interactive via Streamlit pour que vous puissiez :
- **Vous authentifier** sur l'API.
- **Ajouter/modifier des performances** des cyclistes.
- **Consulter les statistiques** en temps réel.
- **Visualiser des tendances** et comparaisons entre différents athlètes.

## Intégration Power BI 📉
Une fois que vous avez collecté les données dans votre base SQLite, vous pouvez les exporter vers Power BI pour :
- Analyser les performances des athlètes.
- Suivre la progression des cyclistes sur le long terme.
- Créer des **tableaux de bord dynamiques** pour vos rapports.

---

## Installation et Configuration 🛠️

### Prérequis
Avant de commencer, vous devez installer quelques dépendances :
```bash
pip install -r requirements.txt

