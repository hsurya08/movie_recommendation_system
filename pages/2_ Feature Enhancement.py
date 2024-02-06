import streamlit as st
import pandas as pd

if 'authenticated' not in st.session_state or st.session_state['authenticated']:
    st.title("Feature Enhancement")
    st.write("""
            Since we are not interested in knowing when the user rated a certain video, we will be deleting the timestamp attribute in this case.
            Merged both the datasets on movieId attribute since it is common between both the dataframes. (100836, 5)
            
            """)
    st.write("""
            **Data Cleaning and Preprocessing**: Handled missing values and normalized ratings to ensure consistency across users.
            
            **Feature Engineering**: By eliminating the 'genre' and 'timestamp' columns, I shifted the focus of the recommendation system towards a pure collaborative filtering approach. This method relies solely on user ratings, assuming that similar users will like similar movies, without considering additional metadata like movie genres or rating times.
            
            **Data Integration**: Merged 'movies.csv' and 'ratings.csv' to create a comprehensive dataset, and created a user-movie matrix essential for collaborative filtering.
        """)
    st.dataframe(st.session_state['combined_df'])    
    st.write("""    
            **Weighted Rating System**: Implemented a system that accounts for both the average rating and the number of ratings a movie has received.
        """)  

    st.dataframe(st.session_state['weighted_df'].reset_index(drop=True))    
else:
    st.error("Please login from the main page")