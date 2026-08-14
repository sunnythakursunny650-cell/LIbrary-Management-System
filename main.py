class Book:
    def __init__(self, book_id, book_name, author):
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.status = "Available"

books = []
def add_book():
    book_id = input("Enter Book ID: ")
    book_name = input("Enter Book Name: ")
    author = input("Enter Author Name: ")

    book = Book(book_id, book_name, author)
    books.append(book)

    print("Book Added Successfully ✅")


def display_books():
    if len(books) == 0:
        print("No Books Available")
    else:
        print("\n--- Library Books ---")

        for book in books:
            print("Book ID:", book.book_id)
            print("Book Name:", book.book_name)
            print("Author:", book.author)
            print("Status:", book.status)
            print("--------------------")

def search_book():
    search = input("Enter Book ID or Book Name to search: ")

    found = False

    for book in books:
        if book.book_id == search or book.book_name.lower() == search.lower():
            print("\nBook Found ✅")
            print("Book ID:", book.book_id)
            print("Book Name:", book.book_name)
            print("Author:", book.author)
            print("Status:", book.status)
            found = True

    if found == False:
        print("Book Not Found ❌")


def issue_book():
    book_id = input("Enter Book ID to issue: ")

    for book in books:
        if book.book_id == book_id:
            if book.status == "Available":
                book.status = "Issued"
                print("Book Issued Successfully ✅")
            else:
                print("Book is already Issued ❌")
            return

    print("Book Not Found ❌")


def return_book():
    book_id = input("Enter Book ID to return: ")

    for book in books:
        if book.book_id == book_id:
            if book.status == "Issued":
                book.status = "Available"
                print("Book Returned Successfully ✅")
            else:
                print("Book is already Available")
            return
        
    print("Book Not Found ❌")

while True:
    print("\n===== Library Management System =====")
    print("1. Add New Book")
    print("2. Display All Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()

    elif choice == "2":
        display_books()

    elif choice == "3":
        search_book()

    elif choice == "4":
        issue_book()

    elif choice == "5":
        return_book()

    elif choice == "6":

        print("Thank you for using Library Management System 📚")

        break
    
    else:
        print("Invalid Choice ❌")