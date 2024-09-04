import streamlit as st


# Conteneur pour le titre et le champ de texte
title_container = st.container()
info_container = st.container()
chat_container = st.container()
input_container = st.container()


# Affichage du titre dans le conteneur
with title_container:
    st.title('Analyseur de sentiment')

with info_container:
    st.write(''' ###### Entrez une phrase ou un paragraphe et on vous déduit le sentiment dominant ..!''')


def send_message():
    if st.session_state.new_message:
        # Récupérer le message saisi
        message = st.session_state.new_message
        # Générer une réponse (ici, on génère une réponse simple)
        prediction = '...'
        response = f"Le sentiment de cette phrase est {prediction}"
        # Afficher le message et la réponse dans le conteneur de discussion
        with chat_container:
            st.write(f''' Vous : {message}''')
            st.write(f"Réponse : {response}")
        # Réinitialiser le champ de saisie
        st.session_state.new_message = ""

# Champ de saisie pour un nouveau message dans le conteneur de saisie
with input_container:
    st.text_input("Entrez un message:", key="new_message", on_change=send_message)











#
# # Initialiser l'état pour stocker les instances de message et réponse
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
#
# # Fonction pour envoyer un message et générer une réponse
# def send_message():
#     if st.session_state.new_message:
#         # Ajoute le message à l'historique avec une réponse
#         response = f"Réponse au message: {st.session_state.new_message}"
#         st.session_state.chat_history.append({
#             'message': st.session_state.new_message,
#             'response': response
#         })
#         # Réinitialiser le champ de saisie
#         st.session_state.new_message = ""
#
#
# # Afficher l'historique des messages et des réponses avec index
# for i, chat in enumerate(st.session_state.chat_history, 1):
#     st.write(f"{i}: Vous- {chat['message']}")
#     st.write(f"Réponse - {chat['response']}")
#
# # Champ de saisie pour un nouveau message
# st.text_input("Entrez un message:", key="new_message", on_change=send_message)
#
#
