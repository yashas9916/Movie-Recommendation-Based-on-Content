#importing libraries
import pandas as pd
import numpy as np
import streamlit as st
import requests
import json

#loading data from the notebook
a=np.load("smaller_array_1.npy")
b=np.load("smaller_array_2.npy")
c=np.load("smaller_array_3.npy")
d=np.load("smaller_array_4.npy")
e=np.load("smaller_array_5.npy")
f=np.load("smaller_array_6.npy")
g=np.load("smaller_array_7.npy")
h=np.load("smaller_array_8.npy")
i=np.load("smaller_array_9.npy")
j=np.load("smaller_array_10.npy")
sig = np.vstack((a,b,c,d,e,f,g,h,i,j))
movies_df=pd.read_csv("finalmovies.csv")
pickle_file_path = "indices.pkl"
indices= pd.read_pickle(pickle_file_path)


st.header('Movie Recommender System')

##used for geting the poster image from online
def fetch_poster(movie_id):
    ##base url 
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)

    ##it will give a json 
    data = requests.get(url)
    data = data.json()

    ##get the information from the poster_path key in the json
    poster_path = data['poster_path']

    ##final path for the poster
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

##used to give recommadation
def give_rec(title, sig=sig):
    # Get the index corresponding to original_title
    idx = indices[title]

    # Get the pairwsie similarity scores 
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies 
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:6]

    # Movie indices
    movie_indices = [i[0] for i in sig_scores]

    # Top 10 most similar movies
    return movies_df['original_title'].iloc[movie_indices]

## dropdowm menu
movie_list =movies_df['original_title'].values
selected_movie = st.selectbox(
    "Select Or Type The Movie You Watched",
    movie_list
)

# Define the number of columns you want
num_columns = 3
# Create a layout context for the columns
columns = st.columns(num_columns)
idx=0


if st.button('Show Recommendation'):
    #input
    a=give_rec(selected_movie)
    
    for i in a:
        with columns[idx % num_columns]:
            st.write("------------")
            st.text(i)
            a=movies_df[movies_df['original_title']==i]['id']
            g=movies_df[movies_df['original_title']==i]['genres']
            l=movies_df[movies_df['original_title']=='Avatar']['language']
            st.image(fetch_poster(a.values[0]))
            color = "#F39C12"
            text="Genres of the movie:"
            colored_text = f"<span style='color:{color}'>{text}</span>"
            st.write(colored_text, unsafe_allow_html=True)
            st.text((g.values[0]))
            color = "#F39C12"
            text="official Language:"
            colored_text = f"<span style='color:{color}'>{text}</span>"
            st.write(colored_text, unsafe_allow_html=True)
            st.write((l.values[0]))
            idx=idx+1

