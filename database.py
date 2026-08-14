import sqlite3
from datetime import datetime

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(
    "library.db",
    check_same_thread=False
)

cursor = conn.cursor()


# =====================================================
# BOOKS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id TEXT PRIMARY KEY,
    book_name TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT DEFAULT 'General',
    status TEXT DEFAULT 'Available',
    issue_date TEXT,
    return_date TEXT
)
""")

conn.commit()


# =====================================================
# ADD BOOK
# =====================================================

def add_book(book_id, book_name, author, category):

    try:

        cursor.execute("""
        INSERT INTO books
        (
            book_id,
            book_name,
            author,
            category,
            status,
            issue_date,
            return_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            book_id,
            book_name,
            author,
            category,
            "Available",
            None,
            None
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False


# =====================================================
# GET ALL BOOKS
# =====================================================

def get_books():

    cursor.execute("""
    SELECT
        book_id,
        book_name,
        author,
        category,
        status,
        issue_date,
        return_date
    FROM books
    ORDER BY book_name
    """)

    return cursor.fetchall()


# =====================================================
# SEARCH BOOKS
# =====================================================

def search_books(search_text):

    search_text = f"%{search_text}%"

    cursor.execute("""
    SELECT
        book_id,
        book_name,
        author,
        category,
        status,
        issue_date,
        return_date
    FROM books
    WHERE
        book_id LIKE ?
        OR book_name LIKE ?
        OR author LIKE ?
        OR category LIKE ?
    ORDER BY book_name
    """, (
        search_text,
        search_text,
        search_text,
        search_text
    ))

    return cursor.fetchall()


# =====================================================
# ISSUE BOOK
# =====================================================

def issue_book(book_id):

    issue_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    UPDATE books
    SET
        status = 'Issued',
        issue_date = ?,
        return_date = NULL
    WHERE
        book_id = ?
        AND status = 'Available'
    """, (
        issue_date,
        book_id
    ))

    conn.commit()

    return cursor.rowcount > 0


# =====================================================
# RETURN BOOK
# =====================================================

def return_book(book_id):

    return_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    UPDATE books
    SET
        status = 'Available',
        return_date = ?
    WHERE
        book_id = ?
        AND status = 'Issued'
    """, (
        return_date,
        book_id
    ))

    conn.commit()

    return cursor.rowcount > 0


# =====================================================
# DELETE BOOK
# =====================================================

def delete_book(book_id):

    cursor.execute("""
    DELETE FROM books
    WHERE book_id = ?
    """, (
        book_id,
    ))

    conn.commit()

    return cursor.rowcount > 0


# =====================================================
# STATISTICS
# =====================================================

def get_statistics():

    cursor.execute(
        "SELECT COUNT(*) FROM books"
    )

    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM books
    WHERE status = 'Available'
    """)

    available = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM books
    WHERE status = 'Issued'
    """)

    issued = cursor.fetchone()[0]

    return total, available, issued


# =====================================================
# CATEGORY STATISTICS
# =====================================================

def get_category_statistics():

    cursor.execute("""
    SELECT
        category,
        COUNT(*)
    FROM books
    GROUP BY category
    ORDER BY COUNT(*) DESC
    """)

    return cursor.fetchall()


# =====================================================
# AUTHOR STATISTICS
# =====================================================

def get_author_statistics():

    cursor.execute("""
    SELECT
        author,
        COUNT(*)
    FROM books
    GROUP BY author
    ORDER BY COUNT(*) DESC
    """)

    return cursor.fetchall()