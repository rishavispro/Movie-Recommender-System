import pickle
import streamlit as st

def recommend(movie):
    

    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        for i in distances[1:6]:
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names
    except (IndexError, KeyError) as e:
        print(f"Error finding movie or similarity: {e}")
        return [] 

st.header('🎬 Movie Recommender System')

try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except (IOError, pickle.PicklingError) as e:
    print(f"Error loading pickled data: {e}")
    st.error("An error occurred while loading the movie data. Please check your pickle files.")
    st.stop()  
if 'selected_movie' not in st.session_state:
    st.session_state['selected_movie'] = None

selected_movie = st.selectbox("Select a Movie you have liked", movies['title'].values)
st.session_state['selected_movie'] = selected_movie

if st.button('Show Recommendation'):
    if st.session_state['selected_movie']:  # Check if a movie is selected
        recommendations = recommend(st.session_state['selected_movie'])
        if recommendations:
            for movie in recommendations:
                st.text(movie)
        else:
            st.info("No recommendations found for this movie.")
