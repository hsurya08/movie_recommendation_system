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