# Library Management System

## Project Overview

This project is a Library Management System built using Django. It provides functionality for library employees to control the book database, manage book issuing and returning processes, and allows users to register on the website to utilize library services.

## Functionality

1. **User Registration**: Library employees can register on the site with required fields such as email, password, full name, personal number, and birth date. Admin can also add employees through the admin panel.

2. **Authorization**: Users of the working group can authorize on the site.

3. **Book Management**:
    - Librarians can add, delete, and modify books.
    - Books can be managed both through the Django admin and via RESTful APIs.
    - Genres and authors are separate models connected to books.
    - Admins can view the history of each book, including who took the book and when it was returned.

4. **Detailed Book List (User Side)**:
    - Users can view detailed information about the book list.
    - The book list includes filtering, searching, and pagination functionalities.
    - Users can reserve a book for 1 day if it is in stock. The reservation is automatically removed if the book is removed from the list.
    - After a book is returned, the librarian can mark in the database that a specific user has returned the corresponding book.

5. **Statistics**:
    - APIs are provided for statistical data, including:
        - The most popular 10 books (the most requested).
        - The number of times each book was taken from the library in the last year.
        - Top 100 books that were returned most often after being late.
        - Top 100 users who are most late in returning the book.

## Libraries Used

- Django: The web framework for building the application.
- Django Rest Framework: Used for writing APIs.
## Bonus Tasks for User Interface

- Email reminders for overdue books.
- User requests for books that are currently checked out.
- Sorting the list of books based on demand.

## Usage

1. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

2. Apply migrations:
    ```bash
    python manage.py migrate
    ```

3. Run the development server:
    ```bash
    python manage.py runserver
    ```

4. Access the application in your browser at `http://localhost:8000`.




