import pandas as pd
import requests
import streamlit as st
import pickle


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + poster_path


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = [(idx, float(score)) for idx, score in sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters  # Return both


# Load data
movies = pd.DataFrame(pickle.load(open("movie_dict.pkl", "rb")))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit UI
st.title("Movie Recommender System 🎬")
selected_movie = st.selectbox("Select a movie", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)  # Now works!
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])



