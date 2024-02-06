import streamlit as st
import pandas as pd
if 'authenticated' not in st.session_state or st.session_state['authenticated']:
    ratings = pd.read_csv('../ratings.csv')
    movies = pd.read_csv('../movies.csv')
    df_r = ratings.copy()
    df_m = movies.copy()
    ratings.drop(['timestamp'], axis=1, inplace=True)
    df_combined = pd.merge(ratings, movies, on = 'movieId')
    st.title("Test Train Split Overview")
    st.dataframe(df_combined.reset_index(drop=True))
    st.write("The code splits user-specific data in a DataFrame into training and testing sets. It first groups the data by 'userId' to separate it for each user. Then, it iterates through each user's data, splitting it into training and testing sets using a 50/50 split ratio. The resulting sets are collected in lists. Finally, all the individual sets are concatenated to create complete training and testing datasets for analysis or machine learning tasks.")
    code = '''
    # Splitting data for each user
    def split_user_data(df):
        # This function splits data for a single user
        test, train = train_test_split(df, test_size=0.5)
        return test, train

    grouped = df_combined.groupby('userId')
    train_frames = []
    test_frames = []
    for user_id, group in grouped:
        test, train = split_user_data(group)
        train_frames.append(train)
        test_frames.append(test)

    # Concatenate all the individual frames to get complete train and test sets
    train_data = pd.concat(train_frames)
    test_data = pd.concat(test_frames)
    '''

    st.header("Test train data split code:")
    st.code(code, language='python')
    st.write("""
            - Train Data: (50566, 5)
            - Test Data: (50270, 5)
            """)
else:
    st.error("Please login from the main page")
