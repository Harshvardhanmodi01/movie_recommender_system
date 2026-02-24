import streamlit as st
import pickle
import requests
import time

# ---------------- FETCH POSTER ----------------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3f9b350f49e31b12c215e56290b88bf8&language=en-US"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=Connection+Error"


# ---------------- LOAD DATA ----------------
movies = pickle.load(open('movies.pkl','rb'))      # contains id, title, tags
similarity = pickle.load(open('similarity.pkl','rb'))


# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_names = []
    recommended_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id   # correct TMDB ID
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        time.sleep(0.2)   # prevent API blocking

    return recommended_names, recommended_posters


# ---------------- UI ----------------
st.title("🎬 Movie Recommender System")

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

# ---------------- BUTTON ----------------
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])