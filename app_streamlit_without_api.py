import streamlit as st
from gensim.models import Word2Vec
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import pickle


# Conteneur pour le titre et le champ de texte
title_container = st.container()
info_container = st.container()
chat_container = st.container()
input_container = st.container()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in ['feel', 'feeling']]
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [str(lemmatizer.lemmatize(token)) for token in filtered_tokens]
    return lemmatized_tokens

def vectorize_text(text, model):
    word_vectors = [model.wv[word] for word in text if word in model.wv]
    if len(word_vectors) > 0:
        return np.mean(word_vectors, axis=0)
    else:
        return np.zeros(model.vector_size)
    

def charger_modele():
    # Charger le modèle à partir du fichier Pickle
    with open('modele.pkl', 'rb') as fichier_modele:
        modele = pickle.load(fichier_modele)
    return modele


def charger_svc():
    # Charger le modèle à partir du fichier Pickle
    with open('svc_classifer.pkl', 'rb') as fichier_modele:
        svc = pickle.load(fichier_modele)
    return svc
    
# Affichage du titre dans le conteneur
with title_container:
    st.title('Analyseur de sentiment')

with info_container:
    st.write(''' ###### Entrez une phrase ou un paragraphe et on vous déduit le sentiment dominant ..!''')


def send_message():
    if st.session_state.new_message:
        # Récupérer le message saisi
        message = st.session_state.new_message
        
        preprocessed_sentence = preprocess_text(message)

        # Étape 2 : Vectoriser la phrase
        sentence_vector = vectorize_text(preprocessed_sentence, charger_modele())

        # Étape 3 : Prédire le label avec les modèles entraînés
        predicted_label_rf = charger_svc().predict([sentence_vector])
        
        if predicted_label_rf == 0:
            predicted_label_rf = 'Triste'
        elif predicted_label_rf == 1 :
            predicted_label_rf = 'Joie'
        elif predicted_label_rf == 3:
            predicted_label_rf = 'Confus'
        else :
            predicted_label_rf = 'Surpris'
        # Générer une réponse (ici, on génère une réponse simple)
        # prediction = '...'
        response = f"Le sentiment de cette phrase est {predicted_label_rf}"
        # Afficher le message et la réponse dans le conteneur de discussion
        with chat_container:
            st.write(f''' Vous : {message}''')
            st.write(f"Réponse : {response}")
        # Réinitialiser le champ de saisie
        st.session_state.new_message = ""

# Champ de saisie pour un nouveau message dans le conteneur de saisie
with input_container:
    st.text_input("Entrez un message:", key="new_message", on_change=send_message)

