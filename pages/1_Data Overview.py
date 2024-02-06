import streamlit as st
import pandas as pd 
import streamlit_authenticator as stauth
import pickle


st.title("Data Overview")

if 'authenticated' not in st.session_state or st.session_state['authenticated']:
    ratings = pd.read_csv('ratings.csv')
    movies = pd.read_csv('movies.csv')
    df_r = ratings.copy()
    df_m = movies.copy()
    ratings.drop(['timestamp'], axis=1, inplace=True)
    df_combined = pd.merge(ratings, movies, on = 'movieId')

    st.session_state['combined_df'] = df_combined.reset_index(drop=True)

    df_n_ratings = pd.DataFrame(df_combined.groupby('title')['rating','movieId'].mean())
    df_n_ratings['movieId'] = df_n_ratings['movieId'].astype(int)
    df_n_ratings['total ratings'] = pd.DataFrame(df_combined.groupby('title')['rating'].count())
    df_n_ratings.rename(columns = {'rating': 'mean ratings'}, inplace=True)

    df_n_ratings.sort_values('total ratings', ascending=False).head(10)
    st.session_state['weighted_df'] = df_n_ratings

    st.write("""
    ## Ratings
    ### “ratings.csv” file has 4 columns:(100836, 4)
    - userId - Unique Id used to represent each user
    - movieId - Unique Id used to represent each movie
    - rating - Rating given to the movie by the corresponding user
    - timestamp - Time at which the rating was recorded.

    ## Movies
    ### "movies" dataframe has 3 columns: (9742, 3) 
    - movieId - Unique Id used to represent each movi
    - title - Name of the movie which is represented by the corresponding movieId.
    - genres - Movie categories

    ### Insights:
    - The lowest possible rating for the film is 0.5, while the highest possible rating is 5.0.
    - The mean score, or average rating, that people have assigned to every movie is 3.5.
    - The userIDs of the users vary from 1 to 610.
    - The movieIds for the films range from 1 to 193609

    ### Different genres in the dataset:
    - 'Adventure': 1263,
    - 'Animation': 611,
    - 'Children': 664,
    - 'Comedy': 3756,
    - 'Fantasy': 779,
    - 'Romance': 1596,
    - 'Drama': 4361,
    - 'Action': 1828,
    - 'Crime': 1199,
    - 'Thriller': 1894,
    - 'Horror': 978,
    - 'Mystery': 573,
    - 'Sci-Fi': 980,
    - 'War': 382,
    - 'Musical': 334,
    - 'Documentary': 440,
    - 'IMAX': 158,
    - 'Western': 167,
    - 'Film-Noir': 87,
    - '(no genres listed)': 34

    """)
    st.image("images/wcld.png", caption='Word Cloud visualization of genres')
    st.image("images/ratings_plot.png", caption='Ratings visualization')
    st.write("It is evident that the majority of the films have ratings of under fifty. Very few movies have received more than 100 ratings.")
else:
    st.error("Please login from the main page")