import streamlit as st
import pickle
import os

# -------------------------------
# Set base directory (folder of app.py)
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, 'model')

# -------------------------------
# Load pickled data safely
def load_pickle(filename):
    file_path = os.path.join(MODEL_DIR, filename)
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return None
    with open(file_path, 'rb') as f:
        return pickle.load(f)

movies = load_pickle('movie_list.pkl')
similarity = load_pickle('similarity.pkl')  # if you have similarity matrix pickled

# -------------------------------
# Streamlit UI
st.title("Movie Recommender System")

if movies is not None:
    movie_list = [movie['title'] for movie in movies]  # adjust if your pickle stores a list of dicts
    selected_movie = st.selectbox("Select a movie:", movie_list)

    if st.button("Recommend"):
        index = next((i for i, m in enumerate(movies) if m['title'] == selected_movie), None)
        if index is not None and similarity is not None:
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            st.write("Top 5 Recommendations:")
            for i in distances[1:6]:
                st.write(movies[i[0]]['title'])
        else:
            st.error("Could not compute recommendations. Check your similarity matrix.")
else:
    st.warning("Movie list not loaded. Make sure 'model/movie_list.pkl' exists.")
