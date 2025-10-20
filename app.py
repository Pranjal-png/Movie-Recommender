import streamlit as st
import pickle
import pandas as pd
import requests
import gzip
import os

# -------------------------------
# ✅ TMDB API Key (stored in Streamlit secrets or environment variable)
# ------------------------------------------------
# Add your API key to `.streamlit/secrets.toml` like this:
# [TMDB]
# API_KEY = "your_actual_api_key_here"
# ------------------------------------------------
try:
    API_KEY = st.secrets["TMDB"]["API_KEY"]
except Exception:
    API_KEY = os.getenv("TMDB_API_KEY")  # fallback if running locally
    if not API_KEY:
        st.error("❌ TMDB API Key not found. Please set it in Streamlit secrets or as an environment variable.")
        st.stop()

# -------------------------------
# Function: Fetch Poster & Movie URL
# -------------------------------
def fetch_poster_and_url(movie_id):
    """Fetch movie poster image URL and TMDB page link."""
    try:
        # Get movie details (including poster_path)
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        response = requests.get(details_url)
        data = response.json()

        poster_path = data.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
        movie_url = data.get("homepage") or f"https://www.themoviedb.org/movie/{movie_id}"

        return poster_url, movie_url
    except Exception as e:
        st.error(f"Error fetching poster for ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster", "#"

# -------------------------------
# Function: Recommend Movies
# -------------------------------
def recommend(movie):
    """Recommend top 5 similar movies."""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_links = []

    for i in movie_list:
        movie_id = int(movies.iloc[i[0]].movie_id)
        title = movies.iloc[i[0]].title

        poster_url, movie_url = fetch_poster_and_url(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster_url)
        recommended_links.append(movie_url)

    return recommended_movies, recommended_posters, recommended_links

# -------------------------------
# Load Data
# -------------------------------
try:
    movies_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
except Exception as e:
    st.error(f"❌ Error loading movies.pkl: {e}")
    st.stop()

try:
    with gzip.open('similarity.pkl.gz', 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    similarity = pickle.load(open('similarity.pkl', 'rb'))

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🎬 Movie Recommender System")
st.write("Discover movies similar to your favorite ones, with live posters and TMDB links!")

selected_movie_name = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend 🎥'):
    with st.spinner("Fetching recommendations..."):
        names, posters, links = recommend(selected_movie_name)

        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(
                    f"""
                    <div style="text-align:center;">
                        <a href="{links[idx]}" target="_blank">
                            <img src="{posters[idx]}" 
                                 style="width:150px; border-radius:10px; box-shadow:0px 4px 10px rgba(0,0,0,0.5);">
                        </a>
                        <p style="font-weight:bold; margin-top:5px;">{names[idx]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
