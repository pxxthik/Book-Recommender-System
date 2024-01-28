import pickle
import numpy as np
import streamlit as st

books_matrix = pickle.load(open("artifacts/books_matrix.pkl", "rb"))
model = pickle.load(open("artifacts/model.pkl", "rb"))
books = pickle.load(open("artifacts/books.pkl", "rb"))

def recommend_books(book_name):
    book_id = np.where(books_matrix.index == book_name)[0][0]
    distances, suggestions = model.kneighbors(books_matrix.iloc[book_id, :].values.reshape(1,-1), n_neighbors=6)
    
    data = []
    for i in range(1, len(suggestions[0])):
        item = {}
        temp_df = books[books['title'] == books_matrix.index[suggestions[0]][i]]
        
        item['title'] = temp_df['title'].values[0]
        item['author'] = temp_df['author'].values[0]
        item['year'] = temp_df['year'].values[0]
        item['num_ratings'] = temp_df['no_of_ratings'].values[0]
        item['image_m'] = temp_df['Image-URL-M'].values[0]
        
        data.append(item)
    
    return data

st.title("Book Recommender System")

selected_book = st.selectbox(
    "Type or Select a Book", books_matrix.index)

if st.button("Recommend"):
    recommendations = recommend_books(selected_book)

    for book in recommendations:
        col1, col2 = st.columns(2)
        with col1:
            st.header(book['title'])
            st.text(f"Author: {book['author']}")
            st.text(f"Year of Publication: {book['year']}")
            st.text(f"{book['num_ratings']}+ Reviews")
        with col2:
            st.image(book['image_m'])