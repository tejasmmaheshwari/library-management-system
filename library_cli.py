import json
import os


FILE_NAME = os.path.join(os.path.dirname(__file__), "books.json")


def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "books": [],
            "issued": []
        }


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def add_book(data):
    print("\n===== ADD BOOK =====")

    book_id = input("Enter book ID: ").strip()

    for book in data["books"]:
        if book["id"] == book_id:
            print("A book with this ID already exists.")
            return

    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()

    book = {
        "id": book_id,
        "title": title,
        "author": author,
        "available": True
    }

    data["books"].append(book)
    save_data(data)

    print("Book added successfully!")


def search_book(data):
    print("\n===== SEARCH BOOK =====")

    search = input("Enter book ID, title, or author: ").strip().lower()

    found = False

    for book in data["books"]:
        if (
            search in book["id"].lower()
            or search in book["title"].lower()
            or search in book["author"].lower()
        ):
            print("\nBook found!")
            print(f"ID: {book['id']}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author']}")

            if book["available"]:
                print("Status: Available")
            else:
                print("Status: Issued")

            found = True

    if not found:
        print("No matching book found.")


def issue_book(data):
    print("\n===== ISSUE BOOKS =====")

    book_ids = input(
        "Enter book IDs to issue (separated by commas): "
    ).split(",")

    borrower = input("Enter borrower's name: ").strip()

    issued_count = 0

    for book_id in book_ids:
        book_id = book_id.strip()

        if not book_id:
            continue

        book_found = False

        for book in data["books"]:

            if book["id"].lower() == book_id.lower():
                book_found = True

                if not book["available"]:
                    print(f"{book['id']} - {book['title']} is already issued.")
                    break

                book["available"] = False

                issue_record = {
                    "book_id": book["id"],
                    "title": book["title"],
                    "borrower": borrower
                }

                data["issued"].append(issue_record)

                print(f"{book['id']} - {book['title']} issued successfully.")
                issued_count += 1

                break

        if not book_found:
            print(f"{book_id} - Book not found.")

    if issued_count > 0:
        save_data(data)
        print(f"\n{issued_count} book(s) issued successfully.")
    else:
        print("\nNo books were issued.")


def return_book(data):
    print("\n===== RETURN BOOKS =====")

    book_ids = input(
        "Enter book IDs to return (separated by commas): "
    ).split(",")

    returned_count = 0

    for book_id in book_ids:
        book_id = book_id.strip()

        if not book_id:
            continue

        book_found = False

        for book in data["books"]:

            if book["id"].lower() == book_id.lower():
                book_found = True

                if book["available"]:
                    print(
                        f"{book['id']} - {book['title']} "
                        "is already available."
                    )
                    break

                book["available"] = True

                for issue in data["issued"]:
                    if issue["book_id"].lower() == book_id.lower():
                        data["issued"].remove(issue)
                        break

                print(
                    f"{book['id']} - {book['title']} "
                    "returned successfully."
                )

                returned_count += 1
                break

        if not book_found:
            print(f"{book_id} - Book not found.")

    if returned_count > 0:
        save_data(data)
        print(f"\n{returned_count} book(s) returned successfully.")
    else:
        print("\nNo books were returned.")


def display_books(data):
    print("\n===== ALL BOOKS =====")

    if not data["books"]:
        print("No books are currently in the library.")
        return

    for book in data["books"]:
        print("\n--------------------")
        print(f"ID: {book['id']}")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")

        if book["available"]:
            print("Status: Available")
        else:
            print("Status: Issued")

    print("--------------------")


def display_issued_books(data):
    print("\n===== ISSUED BOOKS =====")

    if not data["issued"]:
        print("No books are currently issued.")
        return

    for issue in data["issued"]:
        print("\n--------------------")
        print(f"Book ID: {issue['book_id']}")
        print(f"Title: {issue['title']}")
        print(f"Borrower: {issue['borrower']}")

    print("--------------------")


def main():
    data = load_data()

    while True:
        print("\n================================")
        print("     LIBRARY MANAGEMENT SYSTEM")
        print("================================")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View All Books")
        print("6. View Issued Books")
        print("7. Exit")
        print("================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book(data)

        elif choice == "2":
            search_book(data)

        elif choice == "3":
            issue_book(data)

        elif choice == "4":
            return_book(data)

        elif choice == "5":
            display_books(data)

        elif choice == "6":
            display_issued_books(data)

        elif choice == "7":
            print("\nThank you for using the Library Management System!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()