import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud

if 'authenticated' not in st.session_state or st.session_state['authenticated']:
    st.title('Demo:')
    mpl.style.use( 'ggplot' )
    plt.style.use('fivethirtyeight')
    sns.set(context="notebook", palette="dark", style = 'whitegrid' , color_codes=True)
    ratings = pd.read_csv('ratings.csv')
    movies = pd.read_csv('movies.csv')
    df_r = ratings.copy()
    df_m = movies.copy()
    ratings.drop(['timestamp'], axis=1, inplace=True)
    combined_df = pd.merge(ratings, movies, on = 'movieId')
    genres = {} # create a dictionary to store different genre values

    def find_genres():
        for genre in movies['genres']:
            words = genre.split('|')
            for word in words:
                genres[word] = genres.get(word, 0) + 1
                
    find_genres()
    genres['None'] = genres.pop('(no genres listed)')
    wordcloud = WordCloud(width=400, height=200, background_color = 'black', min_font_size=7).generate_from_frequencies(genres)
    df_no_of_ratings = pd.DataFrame(combined_df.groupby('title')[['rating','movieId']].mean())
    df_no_of_ratings['movieId'] = df_no_of_ratings['movieId'].astype(int)
    df_no_of_ratings['total ratings'] = pd.DataFrame(combined_df.groupby('title')['rating'].count())
    df_no_of_ratings.rename(columns = {'rating': 'mean ratings'}, inplace=True)
    df_no_of_ratings.sort_values('total ratings', ascending=False).head(10)
    df_no_of_ratings.sort_values('mean ratings', ascending=False).head(10)
    sns.jointplot(x = 'mean ratings', y = 'total ratings', data = df_no_of_ratings )
    util_matrix = combined_df.pivot_table(index = 'userId', columns = 'title', values = 'rating')
    user_utility_matrix = util_matrix.copy()
    user_utility_matrix = user_utility_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)
    user_utility_matrix.T.corr()

    # Splitting data for each user
    def split_user_data(df):
        # This function splits data for a single user
        test, train = train_test_split(df, test_size=0.5)
        return test, train

    # Group by user and apply the splitting function
    grouped = combined_df.groupby('userId')
    train_frames = []
    test_frames = []
    for user_id, group in grouped:
        test, train = split_user_data(group)
        train_frames.append(train)
        test_frames.append(test)

    # Concatenate all the individual frames to get complete train and test sets
    train_data = pd.concat(train_frames)
    test_data = pd.concat(test_frames)
    inp_user = int(st.text_input("Input User ID", '200'))
    user_corr_mat = user_utility_matrix.T.corr()
    corr_user = user_corr_mat.iloc[inp_user-1]
    corr_user.sort_values(ascending=False, inplace=True)
    corr_user.dropna(inplace = True)
    top50_users_cor = corr_user[1:51]
    watched_mves = train_data[train_data['userId'] == inp_user]
    
    # watched_mves
    unwatched_mves = train_data[~train_data['movieId'].isin(watched_mves['movieId'])]
    unique_unwatched = unwatched_mves['movieId'].unique()
    # unique_unwatched

    filtered_df = df_no_of_ratings[df_no_of_ratings['movieId'].isin(unique_unwatched)]

    # Sort the filtered DataFrame based on total ratings in descending order
    sorted_df = filtered_df.sort_values(by='total ratings', ascending=False)

    # Select the top 20 rows
    top_20 = sorted_df.head(50)

    # Extract the movieId from these top 20 rows
    top_movieIds = top_20['movieId'].tolist()
    # top_movieIds

    def pred_rating(mveID):
        top50_users = top50_users_cor.keys()
        count = 0
        users = list()
        sum_similarity = 0
        weighted_ratings = 0
        for user in top50_users:
            if train_data[ (train_data['userId'] == user) & (train_data['movieId'] == mveID) ]['rating'].sum():
                count +=1
                users.append(user)
        #print(users)
        if len(users) > 0:
            for user in users:
                weighted_ratings += top50_users_cor.loc[user] * train_data[ (train_data['userId'] == user) & 
                                                                    (train_data['movieId'] == mveID) ]['rating'].sum()
                sum_similarity += top50_users_cor.loc[user]
            pred_rat = weighted_ratings / sum_similarity
            return round(pred_rat, 1)
        else:
            return 0

    pred_ratings_arr = []
    for i in top_movieIds:
        pred_ratings_arr.append(pred_rating(i))
    # pred_ratings_arr
    n_recommendations = 5
    def round_to_half(number):
        return round(number * 2) / 2
    rounded_ratings = [round_to_half(rating) for rating in pred_ratings_arr]
    # rounded_ratings
    df_ratings = pd.DataFrame({'movieId': top_movieIds[0:n_recommendations], 'predicted_rating': rounded_ratings[0:n_recommendations]})
    # Merge the DataFrames on movieId
    result_df = pd.merge(df_ratings, movies, on='movieId', how='left')
    result_df['userId'] = inp_user
    err_df = pd.merge(test_data, result_df, on=['userId', 'title'], how='inner')
    err_df['rating_difference'] = abs(err_df['rating'] - err_df['predicted_rating'])
    sum_error = err_df['rating_difference'].sum()
    mean_abs_err = err_df['rating_difference'].abs().mean()
    rmse = np.sqrt((err_df['rating_difference'] ** 2).mean())
    threshold = 3
    err_df['actual_positive'] = err_df['rating'] > threshold
    err_df['predicted_positive'] = err_df['predicted_rating'] > threshold

    # Calculating False Positives and False Negatives
    false_positives = ((err_df['predicted_positive'] == True) & (err_df['actual_positive'] == False)).sum()
    false_negatives = ((err_df['predicted_positive'] == False) & (err_df['actual_positive'] == True)).sum()

    # Calculating Accuracy (defining a tolerance level for accurate predictions, e.g., within 0.5 points)
    tolerance = 0.5
    accuracy = (err_df['rating_difference'].abs() <= tolerance).mean()

    def display_res():
        st.header('Movies rated by the user:')
        watched_mves.rename(columns={'userId': 'User ID', 'title':'Title', 'rating':'Rating'},inplace=True )
        st.dataframe(watched_mves[['User ID', 'Title','Rating' ]].reset_index(drop=True))
        st.header('Movies Recommended to the user:')
        result_df.rename(columns={'genres': 'Genres', 'title':'Title', 'predicted_rating':'Predicted Rating'},inplace=True )
        st.dataframe(result_df[['Title','Genres', 'Predicted Rating']])  
        st.header("Statistics")
        if err_df.empty:
            st.write("No matching movies found in test dataset")
        else:
            st.write("Sum Error:", sum_error)
            st.write("Mean Absolute Error",mean_abs_err)
            st.write("Root Mean Squared Error:",rmse)
            st.write("False Positives:",false_positives)
            st.write("False Negatives:",false_negatives)
            st.write("Accuracy (within,", tolerance," tolerance): ", accuracy * 100, "%")

    trigger = st.button('Submit')
    if trigger:
        display_res()

else:
    st.error("Please login from the main page")
    
