import streamlit as st
import pandas as pd 
import streamlit_authenticator as stauth
from pathlib import Path

st.set_page_config(
    page_title="Movie Recommendation system",
)
st.title("Login Page")
st.session_state['authenticated'] = False
# --- USER AUTHENTICATION ---
names = ["Hemanth Surya", "Ingrid"]
usernames = ["hsurya", "ingrid"]
passwords = ["123", "456"]

ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')
df_r = ratings.copy()
df_m = movies.copy()
ratings.drop(['timestamp'], axis=1, inplace=True)
df_combined = pd.merge(ratings, movies, on = 'movieId')

st.session_state['combined_df'] = df_combined.reset_index(drop=True)

df_n_ratings = pd.DataFrame(df_combined.groupby('title')[['rating','movieId']].mean())
df_n_ratings['movieId'] = df_n_ratings['movieId'].astype(int)
df_n_ratings['total ratings'] = pd.DataFrame(df_combined.groupby('title')['rating'].count())
df_n_ratings.rename(columns = {'rating': 'mean ratings'}, inplace=True)

df_n_ratings.sort_values('total ratings', ascending=False).head(10)
st.session_state['weighted_df'] = df_n_ratings

logged_in = False
if not logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check if the user has submitted the login form
    if st.button("Login"):
        # Check if the username and password are correct
        if username in usernames and password == passwords[usernames.index(username)]:
            st.success(f"Welcome, {names[usernames.index(username)]}!")    
            st.session_state['authenticated'] = True  
            logged_in = True
        #authenticator.logout("Logout", "sidebar")
            #st.sidebar.title(f"Welcome {names[usernames.index(username)]}")
        else:
            st.error("Username/password is incorrect")
            logged_in = False
if logged_in:
    st.sidebar.button("Logout", key="logout_button")
    if st.button("Logout"):
        logged_in = False  # Reset the login flag
        st.success("Logged out successfully.")
