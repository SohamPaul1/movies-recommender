import streamlit as st
import pickle
import requests

def fetch_poster(id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6c386a961bc8b1bd907c25c553232069&language=en-US'.format(id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = sim[idx]
    movies_to_recommend = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    result = []
    poster = []
    for idx, _ in movies_to_recommend:
        result.append(movies.iloc[idx].title)
        poster.append(fetch_poster(movies.iloc[idx].id))
    return result,poster

movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values

sim = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selection = st.selectbox(
    'Here is the list of the movies for you to choose',
    movies_list
)

if st.button('Recommend'):
    movie_name , poster = recommend(selection)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(movie_name[i])
            st.image(poster[i])