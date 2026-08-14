import streamlit as st
import pandas as pd

from database import (
    add_book,
    get_books,
    search_books,
    issue_book,
    return_book,
    delete_book,
    get_statistics,
    get_category_statistics,
    get_author_statistics
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    font-size: 18px;
    color: #777;
    margin-bottom: 25px;
}

.card-title {
    font-size: 15px;
    font-weight: 600;
}

.footer {
    text-align: center;
    padding: 30px 10px;
    margin-top: 50px;
    border-top: 1px solid #ddd;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📚 Library Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Smart Library Management • Book Tracking • Analytics'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Library System")

st.sidebar.markdown(
    "### Navigation"
)

option = st.sidebar.radio(
    "Choose Section",
    [
        "📊 Dashboard",
        "➕ Add Book",
        "📖 All Books",
        "🔍 Search Book",
        "📤 Issue Book",
        "📥 Return Book",
        "🗑️ Delete Book",
        "📈 Analytics"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "💡 Manage books, track availability "
    "and analyze library data."
)

# =========================================================
# DASHBOARD
# =========================================================

if option == "📊 Dashboard":

    st.header("📊 Library Dashboard")

    total, available, issued = get_statistics()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📚 Total Books",
            total
        )

    with col2:
        st.metric(
            "✅ Available",
            available
        )

    with col3:
        st.metric(
            "📕 Issued",
            issued
        )

    st.divider()

    if total == 0:

        st.info(
            "📚 No books found. "
            "Add your first book from **Add Book**."
        )

    else:

        st.subheader("📋 Recent Library Records")

        books = get_books()

        df = pd.DataFrame(
            books,
            columns=[
                "Book ID",
                "Book Name",
                "Author",
                "Category",
                "Status",
                "Issue Date",
                "Return Date"
            ]
        )

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

# =========================================================
# ADD BOOK
# =========================================================

elif option == "➕ Add Book":

    st.header("➕ Add New Book")

    st.write(
        "Enter the details of the new library book."
    )

    with st.form("add_book_form"):

        col1, col2 = st.columns(2)

        with col1:

            book_id = st.text_input(
                "📌 Book ID",
                placeholder="Example: B001"
            )

            book_name = st.text_input(
                "📖 Book Name",
                placeholder="Example: Python Programming"
            )

        with col2:

            author = st.text_input(
                "✍️ Author Name",
                placeholder="Example: Mark Lutz"
            )

            category = st.selectbox(
                "🏷️ Category",
                [
                    "Programming",
                    "Database",
                    "Data Science",
                    "Artificial Intelligence",
                    "Machine Learning",
                    "Mathematics",
                    "Science",
                    "Literature",
                    "History",
                    "General"
                ]
            )

        submitted = st.form_submit_button(
            "➕ Add Book",
            width="stretch"
        )

        if submitted:

            if not book_id.strip():

                st.warning(
                    "Please enter Book ID."
                )

            elif not book_name.strip():

                st.warning(
                    "Please enter Book Name."
                )

            elif not author.strip():

                st.warning(
                    "Please enter Author Name."
                )

            else:

                success = add_book(
                    book_id.strip(),
                    book_name.strip(),
                    author.strip(),
                    category
                )

                if success:

                    st.success(
                        "🎉 Book added successfully!"
                    )

                else:

                    st.error(
                        "❌ This Book ID already exists."
                    )

# =========================================================
# ALL BOOKS
# =========================================================

elif option == "📖 All Books":

    st.header("📖 All Library Books")

    books = get_books()

    if not books:

        st.info(
            "No books available."
        )

    else:

        df = pd.DataFrame(
            books,
            columns=[
                "Book ID",
                "Book Name",
                "Author",
                "Category",
                "Status",
                "Issue Date",
                "Return Date"
            ]
        )

        st.metric(
            "📚 Total Records",
            len(df)
        )

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Library Report",
            data=csv,
            file_name="library_report.csv",
            mime="text/csv",
            width="stretch"
        )

# =========================================================
# SEARCH BOOK
# =========================================================

elif option == "🔍 Search Book":

    st.header("🔍 Search Library")

    search_text = st.text_input(
        "Search by Book ID, Book Name, Author or Category",
        placeholder="Type here..."
    )

    if search_text.strip():

        results = search_books(
            search_text.strip()
        )

        if results:

            df = pd.DataFrame(
                results,
                columns=[
                    "Book ID",
                    "Book Name",
                    "Author",
                    "Category",
                    "Status",
                    "Issue Date",
                    "Return Date"
                ]
            )

            st.success(
                f"🔎 {len(df)} book(s) found."
            )

            st.dataframe(
                df,
                width="stretch",
                hide_index=True
            )

        else:

            st.warning(
                "❌ No matching book found."
            )

# =========================================================
# ISSUE BOOK
# =========================================================

elif option == "📤 Issue Book":

    st.header("📤 Issue Book")

    books = get_books()

    available_books = [
        book for book in books
        if book[4] == "Available"
    ]

    if not available_books:

        st.warning(
            "📚 No books are currently available."
        )

    else:

        book_options = {
            f"{book[0]} — {book[1]}": book[0]
            for book in available_books
        }

        selected = st.selectbox(
            "Select Available Book",
            list(book_options.keys())
        )

        if st.button(
            "📤 Issue Selected Book",
            width="stretch"
        ):

            book_id = book_options[selected]

            success = issue_book(
                book_id
            )

            if success:

                st.success(
                    "✅ Book issued successfully!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Unable to issue this book."
                )

# =========================================================
# RETURN BOOK
# =========================================================

elif option == "📥 Return Book":

    st.header("📥 Return Book")

    books = get_books()

    issued_books = [
        book for book in books
        if book[4] == "Issued"
    ]

    if not issued_books:

        st.info(
            "📚 No books are currently issued."
        )

    else:

        book_options = {
            f"{book[0]} — {book[1]}": book[0]
            for book in issued_books
        }

        selected = st.selectbox(
            "Select Issued Book",
            list(book_options.keys())
        )

        if st.button(
            "📥 Return Selected Book",
            width="stretch"
        ):

            book_id = book_options[selected]

            success = return_book(
                book_id
            )

            if success:

                st.success(
                    "✅ Book returned successfully!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Unable to return this book."
                )

# =========================================================
# DELETE BOOK
# =========================================================

elif option == "🗑️ Delete Book":

    st.header("🗑️ Delete Book")

    books = get_books()

    if not books:

        st.info(
            "No books available."
        )

    else:

        book_options = {
            f"{book[0]} — {book[1]}": book[0]
            for book in books
        }

        selected = st.selectbox(
            "Select Book",
            list(book_options.keys())
        )

        confirm = st.checkbox(
            "⚠️ I confirm that I want to permanently delete this book."
        )

        if st.button(
            "🗑️ Delete Book",
            width="stretch"
        ):

            if not confirm:

                st.warning(
                    "Please confirm deletion first."
                )

            else:

                book_id = book_options[selected]

                success = delete_book(
                    book_id
                )

                if success:

                    st.success(
                        "✅ Book deleted successfully!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Book not found."
                    )

# =========================================================
# ANALYTICS
# =========================================================

elif option == "📈 Analytics":

    st.header("📈 Library Analytics")

    total, available, issued = get_statistics()

    # -----------------------------------------------------
    # STATUS ANALYSIS
    # -----------------------------------------------------

    st.subheader("📊 Book Status")

    status_df = pd.DataFrame(
        {
            "Status": [
                "Available",
                "Issued"
            ],
            "Books": [
                available,
                issued
            ]
        }
    )

    st.bar_chart(
        status_df.set_index("Status")
    )

    st.divider()

    # -----------------------------------------------------
    # CATEGORY ANALYSIS
    # -----------------------------------------------------

    st.subheader("🏷️ Category-wise Books")

    categories = get_category_statistics()

    if categories:

        category_df = pd.DataFrame(
            categories,
            columns=[
                "Category",
                "Books"
            ]
        )

        st.bar_chart(
            category_df.set_index("Category")
        )

        st.dataframe(
            category_df,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No category data available."
        )

    st.divider()

    # -----------------------------------------------------
    # AUTHOR ANALYSIS
    # -----------------------------------------------------

    st.subheader("✍️ Author-wise Books")

    authors = get_author_statistics()

    if authors:

        author_df = pd.DataFrame(
            authors,
            columns=[
                "Author",
                "Books"
            ]
        )

        st.bar_chart(
            author_df.set_index("Author")
        )

        st.dataframe(
            author_df,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No author data available."
        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">

    <h3>📚 Library Management System</h3>

    <p>
    Smart Book Management & Library Analytics
    </p>

    <p>
    Built with <b>Python • SQLite • Streamlit</b>
    </p>

    <p>
    Developed by <b>Sunny Thakur</b> 💫
    </p>

    </div>
    """,
    unsafe_allow_html=True
)