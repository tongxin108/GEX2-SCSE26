## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    load_library,
    save_library,
    find_book
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    category_lower = str(category).strip().lower()
    return [
        book_id
        for book_id, book in books.items()
        if str(book.get("category", "")).strip().lower() == category_lower
    ]


    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    search_lower = str(search_text).strip().lower()
    return [
        book_id
        for book_id, book in books.items()
        if search_lower in str(book.get("title", "")).lower()
    ]


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    if borrower is None or str(borrower).strip() == "":
        return "EMPTY_NAME"

    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    book = books[book_id]

    if not book.get("available"):
        return "NOT_AVAILABLE"

    book["available"] = False
    loans.append({"book_id": book_id, "borrower": borrower})
    return "OK"

    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    if borrower is None or str(borrower).strip() == "":
        return "EMPTY_NAME"

    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    book = books[book_id]

    if book.get("available"):
        return "NOT_ON_LOAN"

    for loan in loans:
        if loan.get("book_id") == book_id:
            loans.remove(loan)
            break

    book["available"] = True
    return "OK"

    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    data = load_library("library.json")
    if data is None:
        print("Could not load library data. Exiting.")
        return

    books = data.get("books", {})
    loans = data.get("loans", [])

    while True:
        print()
        print("=" * 60)
        print("LIBRARY USER SYSTEM")
        print("=" * 60)
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            search_text = input("Enter title or part of title: ")
            results = search_by_title(books, search_text)
            if results:
                print(f"Found {len(results)} book(s):")
                for bid in results:
                    book = books[bid]
                    status = "AVAILABLE" if book.get("available") else "ON LOAN"
                    print(f"  {bid} | {book.get('title')} | {status}")
            else:
                print("No books found.")

        elif choice == "2":
            category = input("Enter category: ")
            results = books_in_category(books, category)
            if results:
                print(f"Found {len(results)} book(s):")
                for bid in results:
                    book = books[bid]
                    status = "AVAILABLE" if book.get("available") else "ON LOAN"
                    print(f"  {bid} | {book.get('title')} | {status}")
            else:
                print("No books found in that category.")

        elif choice == "3":
            search_text = input("Enter book title, author, or ID: ")
            borrower = input("Enter your name: ")
            result = borrow_book(books, loans, search_text, borrower)
            messages = {
                "OK": "Book borrowed successfully!",
                "BOOK_NOT_FOUND": "Error: book not found.",
                "EMPTY_NAME": "Error: borrower name cannot be empty.",
                "NOT_AVAILABLE": "Error: this book is already on loan."
            }
            print(messages.get(result, result))

        elif choice == "4":
            book_title = input("Enter book title, author, or ID: ")
            borrower = input("Enter your name: ")
            result = return_book(books, loans, book_title, borrower)
            messages = {
                "OK": "Book returned successfully!",
                "BOOK_NOT_FOUND": "Error: book not found.",
                "EMPTY_NAME": "Error: borrower name cannot be empty.",
                "NOT_ON_LOAN": "Error: this book is not currently on loan."
            }
            print(messages.get(result, result))

        elif choice == "5":
            save_library(data, "library.json")
            print("Library data saved. Goodbye!")
            break

        else:
            print("Invalid selection. Please choose 1-5.")


if __name__ == "__main__":
    main()


