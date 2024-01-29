import pickle
import numpy as np
import streamlit as st
from streamlit_image_select import image_select

books_matrix = pickle.load(open("artifacts/books_matrix.pkl", "rb"))
model = pickle.load(open("artifacts/model.pkl", "rb"))
books = pickle.load(open("artifacts/books.pkl", "rb"))

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

clicked_book = st.experimental_get_query_params().get('book', [None])[0]
st.set_page_config(
    page_title="Book Recommender System",
    page_icon="📚"
)
st.title("Book Recommender System")

def get_recommendations(book_name):
    recommendations, distances = recommend_books(book_name)
    distances = distances[0]

    i = 1

    for book in recommendations:
        chances = ((1-(distances[i]/distances[-1]))*100)+20
        chances = round(chances, 2)

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


if clicked_book:
    get_recommendations(clicked_book)
    

if not clicked_book:
    selected_book = st.selectbox(
        "Type or Select a Book", books_matrix.index)

    if st.button("Recommend"):
        get_recommendations(selected_book)

    st.header("Popular Books")
    popular = pickle.load(open("artifacts/popular.pkl", "rb"))

    popular_books_image = []
    popular_books_title = []

    for book in popular:
        popular_books_image.append(book[6])
        popular_books_title.append(book[1])

    img = image_select(
        label="Select a cat",
        images=popular_books_image,
        captions=popular_books_title,
        index=0,
        return_value="index"
    )

    if img:
        st.experimental_set_query_params(book=popular_books_title[img])
        st.rerun()