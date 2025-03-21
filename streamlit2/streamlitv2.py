import streamlit as st
import requests

# URL de base de l'API FastAPI
API_BASE_URL = "http://localhost:8000"

# Initialiser les variables d'état de session
if "token" not in st.session_state:
    st.session_state["token"] = None
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# Fonction pour se connecter
def login(username, password):
    try:
        response = requests.post(f"{API_BASE_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state["token"] = response.json()["access_token"]
            st.session_state["current_user"] = username
            st.success("Connexion réussie!")
            st.rerun()
        else:
            st.error("Erreur : " + response.json().get("detail", "Connexion échouée"))
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

# Fonction pour se déconnecter
def logout():
    st.session_state["token"] = None
    st.session_state["current_user"] = None
    st.success("Vous êtes maintenant déconnecté.")

# Fonction pour ajouter une donnée
def add_data(data):
    try:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.post(f"{API_BASE_URL}/performances", json=data, headers=headers)
        if response.status_code == 200:
            st.success("Donnée ajoutée avec succès!")
        else:
            st.error("Erreur : " + response.json().get("detail", "Ajout échoué"))
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

# Fonction pour supprimer une donnée
def delete_data(i):
    try:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.delete(f"{API_BASE_URL}/supprimer/{i}", headers=headers)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error("Erreur : " + response.json().get("detail", "Suppression échouée"))
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

import streamlit as st
import requests

# URL de base de l'API FastAPI
API_BASE_URL = "http://localhost:8000"

# Initialiser les variables d'état de session
if "token" not in st.session_state:
    st.session_state["token"] = None
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# Fonction pour se connecter
def login(username, password):
    try:
        response = requests.post(f"{API_BASE_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state["token"] = response.json()["access_token"]
            st.session_state["current_user"] = username
            st.success("Connexion réussie!")
            st.rerun()
        else:
            st.error("Erreur : " + response.json().get("detail", "Connexion échouée"))
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

# Fonction pour récupérer le meilleur rapport poids/puissance
def get_best_poids_puissance():
    try:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.get(f"{API_BASE_URL}/poidspuissance", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Erreur : " + response.json().get("detail", "Impossible de récupérer les données"))
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")
        return None 

# Fonction pour récupérer l'athlète avec la puissance maximale
def get_puissance_max():
    try:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.get(f"{API_BASE_URL}/puissancemax", headers=headers)
        if response.status_code == 200:
            return response.json()  # Retourner les données du serveur
        else:
            st.error("Erreur : " + response.json().get("detail", "Impossible de récupérer les données"))
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")
        return None     

# Interface utilisateur avec Streamlit
st.title("Application Cyclisme")

if st.session_state["token"] is None:
    # Page de connexion
    st.subheader("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        login(username, password)
else:
    # Navigation entre les différentes pages
    menu = st.sidebar.radio("Menu", ["Accueil", "Meilleur rapport poids/puissance", "Cycliste (Puissance Max)", "Ajouter des données", "Modifier les données", "Supprimer des données", "Déconnexion"])

    if menu == "Accueil":
        st.subheader("Bienvenue sur l'application de gestion des cyclistes")
        st.write("Naviguez via le menu pour effectuer des actions comme ajouter, modifier ou supprimer des données.")

    elif menu == "Meilleur rapport poids/puissance":
        st.subheader("Athlète avec le meilleur rapport poids/puissance")
        best_athlete = get_best_poids_puissance()
        if best_athlete:
            st.write("**Nom :**", best_athlete[0])
            st.write("**ID Cycliste :**", best_athlete[1])
        else:
            st.warning("Aucun résultat disponible.")

    elif menu == "Cycliste (Puissance Max)":
        st.subheader("Athlète avec la puissance maximale")
        puissance_max_athlete = get_puissance_max()
        if puissance_max_athlete:
            st.write("**Nom :**", puissance_max_athlete[0])
            st.write("**ID Cycliste :**", puissance_max_athlete[1])
            st.write("**Puissance Maximale (PPO) :**", puissance_max_athlete[2])
        else:
            st.warning("Aucun résultat disponible.")    
    
    elif menu == "Ajouter des données":
        st.subheader("Ajouter une nouvelle donnée de performance")
        with st.form("ajouter_performance"):
            cyclist_id = st.text_input("ID Cycliste")
            vo2max = st.number_input("VO2Max", min_value=0.0)
            power = st.number_input("Puissance", min_value=0)
            cadence = st.number_input("Cadence", min_value=0)
            hr = st.number_input("Fréquence cardiaque", min_value=0)
            rf = st.number_input("RF", min_value=0)
            if st.form_submit_button("Ajouter"):
                performance_data = {
                    "cyclist_id": cyclist_id,
                    "vo2max": vo2max,
                    "power": power,
                    "cadence": cadence,
                    "hr": hr,
                    "rf": rf
                }
                add_data(performance_data)

    elif menu == "Modifier les données":
        st.subheader("Mettre à jour les données d'un cycliste")
        test_id = st.number_input("ID du test", min_value=1, step=1)

        # Formulaire pour mettre à jour la puissance
        with st.form("modifier_puissance"):
            new_power = st.number_input("Nouvelle puissance", min_value=0)
            if st.form_submit_button("Mettre à jour la puissance"):
                headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                response = requests.put(
                    f"{API_BASE_URL}/modification/{test_id}/power",
                    json={"power": new_power},
                    headers=headers,
                )
                if response.status_code == 200:
                    st.success("Puissance mise à jour avec succès!")
                else:
                    st.error("Erreur : " + response.json().get("detail", "Erreur lors de la mise à jour"))

    elif menu == "Supprimer des données":
        st.subheader("Supprimer une donnée de tests")
        delete_id = st.number_input("ID à supprimer", min_value=1, step=1)
        if st.button("Supprimer"):
            delete_data(delete_id)

    elif menu == "Déconnexion":
        logout()
