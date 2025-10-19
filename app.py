import pickle
import streamlit as st
import requests

# -------------------------------
# Function to fetch movie posters
# -------------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        # Fallback image if poster missing
        return "https://via.placeholder.com/300x450?text=No+Image"

# -------------------------------
# Recommendation function
# -------------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# -------------------------------
# Streamlit UI setup
# -------------------------------
st.title("🎬 Movie Recommender System")

# Load precomputed data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown below:",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # ✅ Use `st.columns` instead of deprecated `st.beta_columns`
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx < len(recommended_movie_names):
            with col:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx])
