# Author : <Chew Rui Hong>
# Admin No / Grp : <230684L / AA2303>

#Help users complete their search
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

#Store the books data in JSON format
import json

#Display tables for better visual appeal
from tabulate import tabulate

#Get time to display on the main menu
from datetime import datetime

restart = False

class ExitToMainMenu(Exception):
    pass


# Completer for ISBNS and TItle
class ISBN_completer(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor(WORD=True)
        for book in books:
            isbn = book["ISBN"]
            if isbn.startswith(word):
                yield Completion(isbn, start_position=-len(word))        
class Title_completer(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor(WORD=True)
        for book in books:
            title = book["Title"]
            if title.lower().startswith(word.lower()):
                yield Completion(title, start_position=-len(word))



# Add books into the library system
def add_book():
    print("\033c", end="")
    try:
        while True:
            # ISBN
            ISBN = custom_input("Enter the ISBN of the book:")
            if not validate_isbn_format(ISBN):
                print(f"The ISBN ({ISBN}) is not valid. Please enter a valid ISBN. (If you are not sure with the format , )")
                print("\n3. Valid ISBN Formats:")
                print("\t- 10-digit ISBN without any dashes.")
                print("\t- 13-digit ISBN with a single dash after the third character (e.g., 978-XXXXXXXXXXX).")
                continue
            elif check_isbn(ISBN):
                print(f"The ISBN ({ISBN}) is already in use. Please enter a unique ISBN.")
                continue
            # Title
            while True:
                Title = custom_input("\nEnter the title of the book:")
                if Title == '':
                    print("\nInvalid title! Please try again")
                else:
                    break
            # Book Type
            while True:    
                type_options = [
                    ["1", "Paperback"],
                    ["2", "Ebook"],
                    ["3", "Hard Cover"],
                ]
                print("\nAdding the type of the book")
                print(tabulate(type_options, headers=["Option", "Description"], tablefmt='grid'))
            
                booktype = custom_input("Enter the type of the book : ")
                if booktype == '1':
                    Book_Type = "Paperback"
                    break
                elif booktype == '2':
                    Book_Type = 'Ebook'
                    break
                elif booktype == '3':
                    Book_Type = 'Hard Cover'
                    break
                else:
                    print("Invalid book type. Please enter a valid book type. Book types:(Paperback, Ebook, Hard Cover)")
            # Quantity
            while True:
                quantity = custom_input("\nEnter the quantity of the book:")
                if check_quantity(quantity):
                    break
                else:
                    print("Invalid quantity of books. Please enter the right number.")
            
            new_book = {"ISBN": ISBN, "Title": Title, "Type": Book_Type, "Quantity": int(quantity)} 
            
            book_data = [new_book]
            
            print("\nThis is the information of the book you are trying to add:")
            print(tabulate(book_data, headers="keys", tablefmt='grid'))
            print('')
            # Ask for confirmation
            while True:
                menu_options = [
                    ["1", "Confirm adding the book to the system"],
                    ["2", "Cancel adding the book to the system"],
                ]  
                print(tabulate(menu_options, headers=["Option", "Description"], tablefmt='grid'))
                confirmation = custom_input("\nDo you want to add this book or cancel adding the book to the system? :")
                if confirmation == '1':
                    books.append(new_book)
                    print("\nBook added successfully!")
                    while True:
                        menu_options = [
                                    ["1", "Add a new book"],
                                    ["q", "Exit to the main menu"],
                                    ]  
                        print(tabulate(menu_options, headers=["Option", "Description"], tablefmt='grid'))
                        confirmation_no = custom_input("\nWould you like to exit to the menu or add a new book? :")
                        if confirmation_no == '1':
                            print("\nAdding a new book\n")
                            break    
                        elif confirmation_no == '2':
                            break
                        else:
                            print("Invalid choice. Please try again.")
                    break
                elif confirmation == '2':
                    while True:
                        menu_options = [
                        ["q", "Exit to the menu"],
                        ["1", "Re-enter the book details"],
                        ]  
                        print("\nBook adding is canceled.")
                        print(tabulate(menu_options, headers=["Option", "Description"], tablefmt='grid'))
                        confirmation_no = custom_input("\nWould you like to exit to the menu or re-enter the book details? :")
                        if confirmation_no == '1':
                            restart = False
                            break
                        elif confirmation_no == '2':
                            restart = True

                            break
                        else:
                            print("Invalid choice. Please try again.")        
                    if not restart:
                        break
                    break
                else:
                    print("Invalid choice. Please try again.")            
    except ExitToMainMenu:
        print("Returning to the main menu.")

# Update book changes in the library system
def update_book():
    
    print("\033c", end="")

    global Book_Type
    
    try:
        while True:
            # Options
            menu_options = [
            ["1", "ISBN"],
            ["2", "Title"],
            ["3", "Exit"],
            ]  
            print("Updating a book")
            print(tabulate(menu_options, headers=["Option", "Description"], tablefmt='grid'))
            search_type = custom_input("\nWould you like to search by ISBN or Title?: ")

            if search_type == "3":
                print("Exiting...")
                return

            if search_type == "1":
                search_key = prompt("\nEnter the ISBN of the book you want to update: ", completer=ISBN_completer())
                key_name = "ISBN"
            elif search_type == "2":
                search_key = prompt("\nEnter the title of the book you want to update: ", completer=Title_completer())
                key_name = "Title"
            else:
                print("Invalid choice. Please try again. (Enter 1 for ISBN, 2 for Title, or 3 to Exit)")
                continue

            book_found = False
            for book in books:
                if book[key_name] == search_key:
                    book_found = True
                    # ISBN
                    while True:
                        ISBN = custom_input("\nEnter the new ISBN of the book (or press enter to keep the current ISBN):")
                        if not ISBN:
                            break
                        elif not validate_isbn_format(ISBN):
                            print(f"The ISBN ({ISBN}) is not valid. Please enter a valid ISBN.")
                            continue
                        elif check_isbn(ISBN):
                            print(f"The ISBN ({ISBN}) is already in use. Please enter a unique ISBN.")
                            continue
                        else:
                            book["ISBN"] = ISBN
                            break
                    # Title   
                    Title = custom_input("\nEnter the new Title of the book (or press enter to keep the current ISBN): ")
                    while True:  
                        if not Title:
                            break
                        else:
                            book["Title"]=Title
                            break
                    # Book Type
                    type_options = [
                            ["1", "Paperback"],
                            ["2", "Ebook"],
                            ["3", "Hard Cover"],
                            ["Enter", "Keep current book type"]
                    ]
                    print("\nAdding the type of the book")
                    print(tabulate(type_options, headers=["Option", "Description"], tablefmt='grid'))
                    while True:    
                        booktype = custom_input("\nEnter the type of the book : ")
                        if not booktype:
                            break
                        elif booktype == '1':
                            Book_Type = "Paperback"
                            break
                        elif booktype == '2':
                            Book_Type = 'Ebook'
                            break
                        elif booktype == '3':
                            Book_Type = 'Hard Cover'
                            break
                        else:
                            print("Invalid book type. Please enter a valid book type. (1. Paperback, 2. Ebook, 3. Hard Cover)")
            
                    # Quantity
                    while True:
                        quantity = custom_input("\nEnter the new quantity of the book (or press enter to keep the current quantity): ")
                        if not quantity:
                            break
                        elif check_quantity(quantity):
                            book["Quantity"] = int(quantity)
                            break
                        else:
                            print("Invalid quantity of books. Please enter the right number.")

                    # Review changes
                    print("\nThis is the updated information of the book:")
                    book_data = [book]
                    print(tabulate(book_data, headers="keys", tablefmt='grid'))


                    
                    # Ask for confirmation
                    options = [
                            ["1", "Confirm saving changes"],
                            ["q", "Cancel saving changes"],
                        ]
                    print("\nAdding the type of the book")
                    print(tabulate(options, headers=["Option", "Description"], tablefmt='grid'))
                    while True:
                        confirmation = custom_input("Do you want to save the changes? :")
                        if confirmation == '1':
                            print("\nBook successfully updated!\n\n\n")
                            break
                        elif confirmation == '2':
                            print("Changes discarded. Please re-enter the book details if you want to update again.")
                            break
                        else:
                            print("\nInvalid input. Please try again.\n")

            if not book_found:
                print(f"\nNo book found with {key_name}: {search_key}. Please try again.\n")
    except ExitToMainMenu:
        print("Returning to the main menu.")

        

# Remove the books from the library system            
def remove_book():
    print("\033c", end="")
    
    try:
        while True:
            # Menu Options
            menu_options = [
            ["1", "ISBN"],
            ["2", "Title"],
            ["3", "Exit"],
            ]
            print("Removing a book")
            print(tabulate(menu_options, headers=["Option", "Description"], tablefmt='grid'))
            search_type = custom_input("\nWould you like to search by ISBN or Title? (Enter 1 for 'ISBN', 2 for 'Title', or 3 to Exit): ")

            if search_type == "3":
                print("Exiting...")
                return

            if search_type == "1":
                search_key = prompt("\nEnter the ISBN of the book you want to remove: ", completer=ISBN_completer())
                key_name = "ISBN"
            elif search_type == "2":
                search_key = prompt("\nEnter the title of the book you want to remove: ", completer=Title_completer())
                key_name = "Title"
            else:
                print("Invalid choice. Please try again. (Enter 1 for ISBN, 2 for Title, or 3 to Exit)")
                continue

            book_found = False
            for book in books:
                if book[key_name] == search_key:
                    book_found = True
                    # Ask for confirmation
                    while True:
                        print(f"The book with {key_name}: {search_key} is being removed.")
                        confirm = custom_input("\nAre you sure ? (Press enter or y to confirm , or press q to quit)")
                        if not confirm or confirm == 'y':
                            books.remove(book)
                            print(f"Book with {key_name}: {search_key} removed successfully!\n")
                            break
                        elif confirm == 'q':
                            break
                        else:
                            print("Invalid input.")
            
            if not book_found:
                print(f"\nNo book found with {key_name}: {search_key}. Please try again.\n")
    except ExitToMainMenu:
        print("Returning to the main menu.")

                
            
# View the books currently in the library system
def view_books():
    
    print("\033c", end="")
    while True:
        if not books:
            print("No books available in the system.")
        else:
            print(f"Total number of books: {len(books)}\n")
            print(tabulate(books, headers='keys', tablefmt='grid'))
        
        enter = input("\nPress enter to leave the help menu:")
        if enter == '':
            break
        else:
            break

# System documentation for users
def system_help():
    print("\033c", end="")

    while True:
        print(
'''
Welcome to the Mini Library Management System version 1.0 Help!

Version 1.0:

1. Current Main Menu Options:
        1. Add New Book: Allows you to add a new book to the library.     
        2. Update Existing Book: Modify the details of an existing book using its ISBN.
        3. Remove Existing Book: Remove a book from the library using its ISBN.
        4. View Books: Displays a list of all the books in the library.   
        5. Help: Provides this help guide.
        6. Exit: Exits the system.

2. ISBN and Title Auto-completion:
        While entering an ISBN or Title, the system provides auto-completion suggestions based on existing books.

3. Valid ISBN Formats:
        1.10-digit ISBN without any dashes.
        2 13-digit ISBN with a single dash after the third character (e.g., 978-XXXXXXXXXXX).

4. Book Quantity:
        Enter a positive integer for the book quantity.

5. Option choosing:
        Most of the options choosing are a range of numbers starting from 1 (e.g. press 1 for yes, or press 2 for no).

6. Users can exit at any time by pressing q for any prompt.
        For example, if the user forgets about the ISBN, the user can press q which exits to the main menu.

Note: Always ensure the ISBN is unique when adding a new book. For updates and removals, ensure the ISBN exists in the system.
'''
        )
        enter = input("\nPress enter to leave to the main menu:")
        if enter == '':
            break
        else:
            break
    
#The main function
def main():
    global books
    load_books_from_json()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    menu_options = [
        ["1", "Add New Book"],
        ["2", "Update Existing Book"],
        ["3", "Remove Existing Book"],
        ["4", "View Books"],
        ["5", "Help"],
        ["6", "Exit"]
    ]
    try:
        while True:
            print("\033c", end="")
            print("Mini Library Management System")
            print(f"Current Time: {current_time}")
            print(tabulate(menu_options, headers=["Option", "Description"], tablefmt='grid'))
            choice = custom_input("Enter your choice: ")
        
            if choice == "1":
                add_book()
            elif choice == "2":
                update_book()
            elif choice == "3":
                remove_book()
            elif choice == "4":
                view_books()
            elif choice == "5":
                system_help()
            elif choice == "6":
                print("Exiting the system...")
                break
            else:
                print("Invalid choice. Please try again.")

        save_books_to_json()
        
    except ExitToMainMenu:
        print("Returning to main menu.")


# Validations
def check_isbn(isbn):
    for book in books:
        if book["ISBN"] == isbn:
            return True
    return False

def validate_isbn_format(isbn):
    original_isbn = isbn
    isbn = isbn.replace("-", "")
    
    if len(isbn) == 10:
        return all(char.isdigit() for char in isbn)
    elif len(isbn) == 13:
        return all(char.isdigit() for char in isbn) and original_isbn[3] == "-"
    else:
        return False
    
def check_quantity(quantity):
    try:
        quantity = int(quantity)
        if quantity > 0:
            return True
        else:
            return False
    except ValueError:
        return False
    
    
# Functions:
def custom_input(prompt):
    user_input = input(prompt)
    if user_input.strip().lower() in ['q', 'exit']:
        raise ExitToMainMenu
    return user_input

# JSON
def save_books_to_json():
    with open("books.json", "w") as file:
        json.dump(books, file)

def load_books_from_json():
    global books
    try:
        with open("books.json", "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        books = [
    {"ISBN": "978-0134846019", "Title": "Data Analytics with Spark Using Python", "Type": "Paper Back", "Quantity": 6},
    {"ISBN": "978-0133316032", "Title": "Children's Reading", "Type": "eBook", "Quantity": 3},
    {"ISBN": "978-1292100142", "Title": "Global Marketing, 7th Edition", "Type": "eBook", "Quantity": 8},
    {"ISBN": "978-1587147029", "Title": "CCNA Cyber Ops SECFND #210-250 Official Cert Guide", "Type": "Hard Cover", "Quantity": 5},
    {"ISBN": "0306406152", "Title": "Learn Data Analytics in 100 days", "Type": "Paper Back", "Quantity": 10}   
    ]





    
main()
#500 Mark! :) THis does not affect the user system , only for developers and lectuers to see :)