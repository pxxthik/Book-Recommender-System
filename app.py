import pickle
import numpy as np
import streamlit as st

books_matrix = pickle.load(open("artifacts/books_matrix.pkl", "rb"))
model = pickle.load(open("artifacts/model.pkl", "rb"))
books = pickle.load(open("artifacts/books.pkl", "rb"))
popular = pickle.load(open("artifacts/popular.pkl", "rb"))

def recommend_books(book_name):
    book_id = np.where(books_matrix.index == book_name)[0][0]
    distances, suggestions = model.kneighbors(books_matrix.iloc[book_id, :].values.reshape(1,-1), n_neighbors=books_matrix.shape[0])
    
    data = []
    for i in range(1, 6):
        item = {}
        temp_df = books[books['title'] == books_matrix.index[suggestions[0]][i]]
        
        item['title'] = temp_df['title'].values[0]
        item['author'] = temp_df['author'].values[0]
        item['year'] = temp_df['year'].values[0]
        item['num_ratings'] = temp_df['no_of_ratings'].values[0]
        item['image_m'] = temp_df['Image-URL-M'].values[0]
        
        data.append(item)
    
    return data, distances

st.set_page_config(
    page_title="Book Recommender System",
    page_icon="📚"
)

st.title("Book Recommender System")

selected_book = st.selectbox(
    "Type or Select a Book", books_matrix.index)

if st.button("Recommend"):
    recommendations, distances = recommend_books(selected_book)
    distances = distances[0]

    i = 1

    for book in recommendations:
        chances = round((1-(distances[i]/distances[-1]))*100, 2)

        chances += 20

        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.header(book['title'])
            st.text(f"Year of Publication: {book['year']}")
            st.text(f"{book['num_ratings']}+ Reviews")
            st.metric("People also read this book by", "", f"{chances}%")
        with col2:
            st.image(book['image_m'])
            st.text(f"Author: {book['author']}")
        
        st.markdown("""---""")
        i+= 1

st.header("Popular Books")

for i in range(5):
    k = i*5
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(popular[k][6])
        st.text(popular[k][1])
    with col2:
        st.image(popular[k+1][6])
        st.text(popular[k+1][1])
    with col3:
        st.image(popular[k+2][6])
        st.text(popular[k+2][1])
    with col4:
        st.image(popular[k+3][6])
        st.text(popular[k+3][1])
    with col5:
        st.image(popular[k+4][6])
        st.text(popular[k+4][1])