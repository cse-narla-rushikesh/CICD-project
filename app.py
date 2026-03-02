
from flask import Flask, render_template, request
import pickle
import numpy as np

import pickle
import os

model_path = os.path.abspath("model.pkl")
print(f"📦 Trying to load model from: {model_path}")

with open(model_path, 'rb') as f:
    model_data = pickle.load(f)
app = Flask(__name__)

# Load the model
with open('model.pkl', 'rb') as f:
    model_data = pickle.load(f)

movies = model_data['movies']
similarity = model_data['similarity']

def recommend(movie_title):
    movie_title = movie_title.lower()
    matches = movies[movies['title'].str.lower() == movie_title]

    if matches.empty:
        return []

    index = matches.index[0]
    distances = list(enumerate(similarity[index]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended_titles = [movies.iloc[i[0]].title for i in sorted_movies]
    return recommended_titles

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    error = None

    if request.method == 'POST':
        movie_name = request.form['movie']
        recommendations = recommend(movie_name)
        if not recommendations:
            error = "Movie not found. Please try another."

    return render_template('index.html', recommendations=recommendations, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

