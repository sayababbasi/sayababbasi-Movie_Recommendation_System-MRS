# we are using Stem-let you can used Flask
import requests
import streamlit as st
import pickle as pk
import pandas as pd


movie_dict = pk.load(open('Movies_dict.pkl', 'rb'))
similarity = pk.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a74d55d95a43539bab325251359f7c98'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended_movies = []
    recommended_movies_poster = []
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

st.title('Movies Recommendations SYSTEM')
st.subheader('BY SAYAB ABBASI')
selected_movie_name = st.selectbox('Select or Enter Movie Name', movies['title'].values)

if st.button('Recommand'):
    names,posters = recommend(selected_movie_name)

    # Create columns
    cols = st.columns(5)
    # Loop through columns and data
    for i, col in enumerate(cols):
        with col:
            st.image(posters[i])
            st.header(names[i])

