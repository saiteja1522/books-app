import streamlit as st
import pandas as pd

st.set_page_config(page_title="📚 Book Explorer", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f4f1ee;
    }
    .block-container {
        padding: 2rem 2rem 2rem;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #3e3e3e;
    }
    .stSelectbox > div > div {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Book Explorer")

@st.cache_data(show_spinner=True)
def load_merged(path: str = ".") -> pd.DataFrame:
    ratings = pd.read_csv(f"{path}/Ratings.csv", encoding="latin-1")
    books   = pd.read_csv(f"{path}/Books.csv",   encoding="latin-1")
    users   = pd.read_csv(f"{path}/Users.csv",   encoding="latin-1")
    ratings = ratings[ratings["Book-Rating"] > 0]
    return ratings.merge(books, on="ISBN").merge(users, on="User-ID")

with st.spinner("🔄 Loading data …"):
    df = load_merged()

mode = st.radio("📂 Explore by:", ["Book Title", "Author", "Publisher"], horizontal=True)

if mode == "Book Title":
    options = sorted(df["Book-Title"].dropna().unique())
    title = st.selectbox("📖 Select Book Title", options)
    selected = df[df["Book-Title"] == title]
    if not selected.empty:
        row = selected.iloc[0]
        st.markdown(f"### 📘 Details for **{title}**")
        cols = st.columns([1, 4])
        with cols[0]:
            st.image(row["Image-URL-M"], width=100)
        with cols[1]:
            st.markdown(f"**Author:** {row['Book-Author']}")
            st.markdown(f"**Year:** {row['Year-Of-Publication']}")
            st.markdown(f"**Publisher:** {row['Publisher']}")
            st.markdown(f"**Rating:** {row['Book-Rating']} ⭐")
            st.markdown(f"**User Age:** {row['Age']}")
            st.markdown(f"**Location:** {row['Location']}")

        # Recommender
        author = row["Book-Author"]
        recs = df[(df["Book-Author"] == author) & (df["Book-Title"] != title)]["Book-Title"].unique()
        st.markdown(f"#### 📘 More by **{author}**")
        for book in recs[:5]:
            st.markdown(f"- {book}")

elif mode == "Author":
    authors = sorted(df["Book-Author"].dropna().unique())
    author = st.selectbox("✍️ Select Author", authors)
    books_by_author = df[df["Book-Author"] == author]
    top_books = books_by_author.groupby("Book-Title")["Book-Rating"].mean().reset_index()
    top_books = top_books.sort_values("Book-Rating", ascending=False).head(5)
    st.markdown(f"### ✍️ Top 5 books by **{author}**")
    for title in top_books["Book-Title"]:
        info = books_by_author[books_by_author["Book-Title"] == title].iloc[0]
        cols = st.columns([1, 4])
        with cols[0]:
            st.image(info["Image-URL-M"], width=100)
        with cols[1]:
            st.markdown(f"**Title:** {title}")
            st.markdown(f"**Publisher:** {info['Publisher']}")
            st.markdown(f"**Year:** {info['Year-Of-Publication']}")
            st.markdown(f"**Avg Rating:** {round(top_books[top_books['Book-Title']==title]['Book-Rating'].values[0], 2)} ⭐")
        st.markdown("---")

elif mode == "Publisher":
    publishers = sorted(df["Publisher"].dropna().unique())
    publisher = st.selectbox("🏢 Select Publisher", publishers)
    books_by_pub = df[df["Publisher"] == publisher]
    top_books = books_by_pub.groupby("Book-Title")["Book-Rating"].mean().reset_index()
    top_books = top_books.sort_values("Book-Rating", ascending=False).head(5)
    st.markdown(f"### 🏢 Top 5 books from **{publisher}**")
    for title in top_books["Book-Title"]:
        info = books_by_pub[books_by_pub["Book-Title"] == title].iloc[0]
        cols = st.columns([1, 4])
        with cols[0]:
            st.image(info["Image-URL-M"], width=100)
        with cols[1]:
            st.markdown(f"**Title:** {title}")
            st.markdown(f"**Author:** {info['Book-Author']}")
            st.markdown(f"**Year:** {info['Year-Of-Publication']}")
            st.markdown(f"**Avg Rating:** {round(top_books[top_books['Book-Title']==title]['Book-Rating'].values[0], 2)} ⭐")
        st.markdown("---")

st.markdown("---")
st.caption("")
