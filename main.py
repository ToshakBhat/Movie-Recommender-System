import streamlit as st
import pickle

import pandas as pd
import requests

movies_dict = pickle.load(open("movies_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=0ade63f571c991817fb936564f792a10&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended = []
    recommended_movies_poster = []
    for i in movies_list:
        index = i[0]
        movie_id = movies.iloc[index].movie_id

        recommended.append(movies.iloc[index].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended,recommended_movies_poster
selected_movie_name = st.selectbox(
    "Enter your favourite movie to get recommendations :)",
    movies['title'].values
)
similarity = pickle.load(open('similarity.pkl','rb'))

if st.button('Recommend'):
    recommendations,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
    col = [col1, col2, col3, col4, col5]

    for i in recommendations[0:5]:
        #st.write(i)
        with col[recommendations.index(i)]:
            #st.text(i)
            st.image(posters[recommendations.index(i)])

    col6, col7, col8, col9, col10 = st.columns(5, gap="medium")
    col = [col6, col7, col8, col9, col10]
    j  = 0
    for i in recommendations[5:11]:
        #st.write(i)
        with col[j]:
            #st.text(i)
            st.image(posters[recommendations.index(i)])
            j += 1
