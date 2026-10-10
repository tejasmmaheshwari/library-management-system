import tkinter as tk
from tkinter import ttk, messagebox

import library_cli


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Load existing library data
        self.data = library_cli.load_data()

        self.create_widgets()
        self.refresh_books()

    def create_widgets(self):
        # Main title
        title = tk.Label(
            self.root,
            text="LIBRARY MANAGEMENT SYSTEM",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Book",
            width=18,
            command=self.add_book_window
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Search Book",
            width=18,
            command=self.search_book_window
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Issue Book",
            width=18,
            command=self.issue_book_window
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Return Book",
            width=18,
            command=self.return_book_window
        ).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="View All Books",
            width=18,
            command=self.refresh_books
        ).grid(row=2, column=0, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="View Issued Books",
            width=18,
            command=self.show_issued_books
        ).grid(row=2, column=1, padx=5, pady=5)

        # Book table
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        columns = ("ID", "Title", "Author", "Status")

        self.book_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        self.book_table.heading("ID", text="Book ID")
        self.book_table.heading("Title", text="Title")
        self.book_table.heading("Author", text="Author")
        self.book_table.heading("Status", text="Status")

        self.book_table.column("ID", width=100)
        self.book_table.column("Title", width=250)
        self.book_table.column("Author", width=250)
        self.book_table.column("Status", width=120)

        self.book_table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.book_table.yview
        )

        scrollbar.pack(side="right", fill="y")

        self.book_table.configure(yscrollcommand=scrollbar.set)

        # Exit button
        tk.Button(
            self.root,
            text="Exit",
            width=20,
            command=self.root.destroy
        ).pack(pady=10)

    def refresh_data(self):
        self.data = library_cli.load_data()

    def refresh_books(self):
        self.refresh_data()

        # Remove existing rows
        for item in self.book_table.get_children():
            self.book_table.delete(item)

        # Add books to table
        for book in self.data["books"]:
            status = "Available" if book["available"] else "Issued"

            self.book_table.insert(
                "",
                "end",
                values=(
                    book["id"],
                    book["title"],
                    book["author"],
                    status
                )
            )

    def add_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Book")
        window.geometry("400x300")
        window.resizable(False, False)

        tk.Label(
            window,
            text="Add New Book",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        tk.Label(window, text="Book ID").pack()
        id_entry = tk.Entry(window, width=35)
        id_entry.pack(pady=5)

        tk.Label(window, text="Title").pack()
        title_entry = tk.Entry(window, width=35)
        title_entry.pack(pady=5)

        tk.Label(window, text="Author").pack()
        author_entry = tk.Entry(window, width=35)
        author_entry.pack(pady=5)

        def add():
            book_id = id_entry.get().strip()
            title = title_entry.get().strip()
            author = author_entry.get().strip()

            if not book_id or not title or not author:
                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields."
                )
                return

            for book in self.data["books"]:
                if book["id"].lower() == book_id.lower():
                    messagebox.showerror(
                        "Duplicate ID",
                        "A book with this ID already exists."
                    )
                    return

            book = {
                "id": book_id,
                "title": title,
                "author": author,
                "available": True
            }

            self.data["books"].append(book)
            library_cli.save_data(self.data)

            messagebox.showinfo(
                "Success",
                "Book added successfully!"
            )

            window.destroy()
            self.refresh_books()

        tk.Button(
            window,
            text="Add Book",
            width=20,
            command=add
        ).pack(pady=15)

    def search_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Search Book")
        window.geometry("500x400")
        window.resizable(False, False)

        tk.Label(
            window,
            text="Search Book",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        tk.Label(
            window,
            text="Enter Book ID, Title, or Author"
        ).pack()

        search_entry = tk.Entry(window, width=40)
        search_entry.pack(pady=10)

        results = tk.Text(
            window,
            width=55,
            height=15
        )
        results.pack(pady=10)

        def search():
            self.refresh_data()

            search_text = search_entry.get().strip().lower()

            if not search_text:
                messagebox.showwarning(
                    "Search",
                    "Please enter something to search."
                )
                return

            results.delete("1.0", tk.END)

            found = False

            for book in self.data["books"]:
                if (
                    search_text in book["id"].lower()
                    or search_text in book["title"].lower()
                    or search_text in book["author"].lower()
                ):
                    status = (
                        "Available"
                        if book["available"]
                        else "Issued"
                    )

                    results.insert(
                        tk.END,
                        f"ID: {book['id']}\n"
                        f"Title: {book['title']}\n"
                        f"Author: {book['author']}\n"
                        f"Status: {status}\n"
                        f"{'-' * 40}\n"
                    )

                    found = True

            if not found:
                results.insert(
                    tk.END,
                    "No matching book found."
                )

        tk.Button(
            window,
            text="Search",
            width=20,
            command=search
        ).pack()

    def issue_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Issue Books")
        window.geometry("500x350")
        window.resizable(False, False)

        tk.Label(
            window,
            text="Issue Books",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        tk.Label(
            window,
            text="Book IDs (separated by commas)"
        ).pack()

        ids_entry = tk.Entry(window, width=45)
        ids_entry.pack(pady=8)

        tk.Label(
            window,
            text="Borrower's Name"
        ).pack()

        borrower_entry = tk.Entry(window, width=45)
        borrower_entry.pack(pady=8)

        def issue():
            self.refresh_data()

            book_ids = ids_entry.get().split(",")
            borrower = borrower_entry.get().strip()

            if not borrower:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter the borrower's name."
                )
                return

            issued_count = 0
            messages = []

            for book_id in book_ids:
                book_id = book_id.strip()

                if not book_id:
                    continue

                found = False

                for book in self.data["books"]:
                    if book["id"].lower() == book_id.lower():
                        found = True

                        if not book["available"]:
                            messages.append(
                                f"{book['id']} is already issued."
                            )
                            break

                        book["available"] = False

                        self.data["issued"].append({
                            "book_id": book["id"],
                            "title": book["title"],
                            "borrower": borrower
                        })

                        issued_count += 1

                        messages.append(
                            f"{book['id']} issued successfully."
                        )

                        break

                if not found:
                    messages.append(
                        f"{book_id} was not found."
                    )

            if issued_count > 0:
                library_cli.save_data(self.data)
                self.refresh_books()

            messagebox.showinfo(
                "Issue Result",
                "\n".join(messages)
            )

            if issued_count > 0:
                window.destroy()

        tk.Button(
            window,
            text="Issue Books",
            width=20,
            command=issue
        ).pack(pady=20)

    def return_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Return Books")
        window.geometry("500x300")
        window.resizable(False, False)

        tk.Label(
            window,
            text="Return Books",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        tk.Label(
            window,
            text="Book IDs (separated by commas)"
        ).pack()

        ids_entry = tk.Entry(window, width=45)
        ids_entry.pack(pady=10)

        def return_books():
            self.refresh_data()

            book_ids = ids_entry.get().split(",")

            returned_count = 0
            messages = []

            for book_id in book_ids:
                book_id = book_id.strip()

                if not book_id:
                    continue

                found = False

                for book in self.data["books"]:
                    if book["id"].lower() == book_id.lower():
                        found = True

                        if book["available"]:
                            messages.append(
                                f"{book['id']} is already available."
                            )
                            break

                        book["available"] = True

                        for issue in self.data["issued"]:
                            if (
                                issue["book_id"].lower()
                                == book_id.lower()
                            ):
                                self.data["issued"].remove(issue)
                                break

                        returned_count += 1

                        messages.append(
                            f"{book['id']} returned successfully."
                        )

                        break

                if not found:
                    messages.append(
                        f"{book_id} was not found."
                    )

            if returned_count > 0:
                library_cli.save_data(self.data)
                self.refresh_books()

            messagebox.showinfo(
                "Return Result",
                "\n".join(messages)
            )

            if returned_count > 0:
                window.destroy()

        tk.Button(
            window,
            text="Return Books",
            width=20,
            command=return_books
        ).pack(pady=20)

    def show_issued_books(self):
        self.refresh_data()

        window = tk.Toplevel(self.root)
        window.title("Issued Books")
        window.geometry("600x450")
        window.resizable(False, False)

        tk.Label(
            window,
            text="Currently Issued Books",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        columns = ("ID", "Title", "Borrower")

        table = ttk.Treeview(
            window,
            columns=columns,
            show="headings",
            height=15
        )

        table.heading("ID", text="Book ID")
        table.heading("Title", text="Title")
        table.heading("Borrower", text="Borrower")

        table.column("ID", width=100)
        table.column("Title", width=250)
        table.column("Borrower", width=150)

        table.pack(padx=20, pady=10)

        if not self.data["issued"]:
            messagebox.showinfo(
                "Issued Books",
                "No books are currently issued."
            )
            window.destroy()
            return

        for issue in self.data["issued"]:
            table.insert(
                "",
                "end",
                values=(
                    issue["book_id"],
                    issue["title"],
                    issue["borrower"]
                )
            )


def main():
    root = tk.Tk()
    LibraryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()