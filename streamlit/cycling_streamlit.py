import streamlit as st
import requests
import json

# URL de l'API FastAPI
API_URL = "http://127.0.0.1:8086"  # Assure-toi que l'URL de ton API est correcte

# Fonction pour obtenir le token d'authentification
def get_token(username, password):
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        st.error("Erreur lors de la connexion")
        return None

# Fonction pour vérifier si l'utilisateur est authentifié
def check_authentication(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/coach/performances", headers=headers)
    if response.status_code == 401:
        st.error("Authentification requise")
        return False
    return True

# Interface de connexion
st.title("Tableau de bord Cyclisme")

# Demander le nom d'utilisateur et le mot de passe
username = st.text_input("Nom d'utilisateur")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):
    token = get_token(username, password)
    if token:
        st.session_state["token"] = token
        st.success("Connexion réussie!")

# Si l'utilisateur est connecté, permettre l'accès aux données
if "token" in st.session_state:
    token = st.session_state["token"]
    
    if check_authentication(token):
        st.sidebar.title("Options")
        
        # Afficher les performances des athlètes
        if st.sidebar.button("Voir les performances"):
            response = requests.get(f"{API_URL}/coach/performances", headers={"Authorization": f"Bearer {token}"})
            performances = response.json()
            if performances:
                st.write("Performances des cyclistes:")
                st.json(performances)
            else:
                st.write("Aucune performance à afficher.")
        
        # Ajouter une performance
        st.sidebar.title("Ajouter une performance")
        cyclist_id = st.number_input("ID du cycliste", min_value=1)
        power = st.number_input("Puissance")
        vo2max = st.number_input("VO2max")
        cadence = st.number_input("Cadence")
        hr = st.number_input("HR")
        rf = st.number_input("RF")
        
        if st.sidebar.button("Ajouter la performance"):
            performance_data = {
                "cyclist_id": cyclist_id,
                "power": power,
                "vo2max": vo2max,
                "cadence": cadence,
                "hr": hr,
                "rf": rf
            }
            response = requests.post(f"{API_URL}/performances", json=performance_data, headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 200:
                st.success("Performance ajoutée avec succès!")
            else:
                st.error("Erreur lors de l'ajout de la performance.")
        
        # Statistiques - Athlète avec le meilleur rapport poids/puissance
        if st.sidebar.button("Voir athlète avec le meilleur rapport poids/puissance"):
            response = requests.get(f"{API_URL}/poidspuissance", headers={"Authorization": f"Bearer {token}"})
            result = response.json()
            st.write("Athlète avec le meilleur rapport poids/puissance :")
            st.json(result)
        
        # Statistiques - Athlète avec la meilleure puissance
        if st.sidebar.button("Voir athlète avec la meilleure puissance"):
            response = requests.get(f"{API_URL}/puissancemax", headers={"Authorization": f"Bearer {token}"})
            result = response.json()
            st.write("Athlète avec la meilleure puissance :")
            st.json(result)
        
        # Modification des performances
        st.sidebar.title("Modifier une performance")
        test_id = st.number_input("ID de la performance à modifier", min_value=1)
        new_power = st.number_input("Nouvelle Puissance")
        
        if st.sidebar.button("Modifier la performance"):
            updated_data = {"power": new_power}
            response = requests.put(f"{API_URL}/modification/{test_id}/power", json=updated_data, headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 200:
                st.success("Performance mise à jour avec succès!")
            else:
                st.error("Erreur lors de la mise à jour de la performance.")
        
        # Suppression d'une performance
        st.sidebar.title("Supprimer une performance")
        delete_id = st.number_input("ID de la performance à supprimer", min_value=1)
        
        if st.sidebar.button("Supprimer la performance"):
            response = requests.delete(f"{API_URL}/supprimer/{delete_id}", headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 200:
                st.success("Performance supprimée avec succès!")
            else:
                st.error("Erreur lors de la suppression de la performance.")
