import streamlit as st

if st.session_state['authenticated']:
    st.title("Recommendation Abstract")
    st.write("""
        ## User-Based Collaborative Filtering (CF) in Movie Recommendations

        I implemented a movie recommendation system using User-Based Collaborative Filtering (User-Based CF). This decision was based on several key considerations, tailored to the project's specific needs and the inherent nature of movie recommendations.

        ### Nature of Movie Preferences
        - **Shared Interests:** Movie preferences often align within groups of users. If someone agrees on one movie with another user, they are likely to have similar tastes in other movies. User-Based CF leverages this shared taste effectively.
        - **Dynamic Content Consumption:** Movies are a dynamic domain where user preferences can evolve over time. User-Based CF adapts to these changes by continually integrating new user ratings.

        ### Data Characteristics
        - **Rich User Interaction Data:** My system has access to substantial user ratings and reviews, providing a rich dataset for understanding user preferences.
        - **User Engagement:** Engaging users through personalized recommendations can encourage more ratings and reviews, which in turn, enhances the recommendation system further.

        ### Implementation Considerations
        - **Simplicity and Interpretability:** User-Based CF is relatively straightforward to implement and understand. It provides transparent recommendations based on visible similarities between users, which can be more interpretable to end-users.
        - **Community Aspect:** Movies are often watched in social settings. Recommendations based on similar users can inadvertently capture the social aspect of movie-watching, suggesting films that might be appealing in group settings.

        ### Scalability and Performance
        - **Scalability:** Although User-Based CF can be computationally intensive, I designed the system to handle this through efficient data structures and algorithms.
        - **Avoiding Cold Start:** My initial user base is sufficiently large to avoid the cold start problem, making User-Based CF a viable option from the start.

        ### Room for Evolution
        - **Hybrid Systems:** Looking ahead, there's potential to evolve into a hybrid model, integrating User-Based CF with other approaches to further enhance recommendation accuracy.
        
        ## Conclusion:
        In conclusion, the used collaborative filtering in the movie recommendation system allows it to provide users with customized movie recommendations. The algorithm provides precise movie suggestions by examining user ratings and detecting similar user profiles. With the help of the Streamlit integration, customers can view both their recommended and rated movies and submit their choices on an easy-to-use interface. Evaluation metrics also guarantee the validity of the recommendations.
        """)
else:
    st.error("Please login from the main page")