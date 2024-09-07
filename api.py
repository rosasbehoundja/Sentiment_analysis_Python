from flask import Flask, request, jsonify
import pickle
from gensim.models import Word2Vec
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import pickle


app = Flask(__name__)


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

@app.route('/predict', methods=['POST'])

def predict():
    data = request.json
    message = data['message']
    preprocessed_sentence = preprocess_text(message)
    sentence_vector = vectorize_text(preprocessed_sentence, charger_modele())
    prediction = charger_svc().predict([sentence_vector])
    return jsonify({'prediction': int(prediction[0])})


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)

