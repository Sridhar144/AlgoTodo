**To-Do List Application**

This is a Django-based web application designed for managing a simple to-do list. It provides users with the ability to create, read, update, and delete tasks, and also supports tagging tasks with custom tags. The application includes authentication and authorization using JWT (JSON Web Tokens) to secure the API.

**Features**

- **Task Management:**
- Create, Read, Update, and Delete tasks.
- Each task includes the following attributes:
- **Timestamp:** The time the task was created.
- **Title:** The task's title (up to 100 characters).
- **Description:** A detailed description of the task (up to 1000 characters).
- **DueDate:** An optional field for setting a due date.
- **Tags:** One or more tags that can be added to a task (many-to-many relationship).
- **Status:** One of the predefined statuses:
  - OPEN (default)
  - WORKING
  - PENDING REVIEW
  - COMPLETED
  - OVERDUE
  - CANCELLED
- **Authentication and Authorization:**
- JWT-based authentication.
- Role-based authorization (e.g., Admin, User) with permissions assigned to different users.
- **Admin Interface:**
- An admin panel with task management and validation rules.
- Custom changelist view with filters for each model.
- Appropriate validation checks for mandatory fields.
- **API Endpoints (Django REST Framework):**
- POST /api/tasks/: Create a new task.
- GET /api/tasks/{id}/: Retrieve a specific task.
- GET /api/tasks/: Retrieve all tasks.
- PUT /api/tasks/{id}/: Update a specific task.
- DELETE /api/tasks/{id}/: Delete a specific task.

**Technologies Used**

- **Backend:** Python 3.11+, Django 4.2.7+, Django REST Framework 3.14.0+
- **Authentication:** Simple JWT (JSON Web Token)
- **Database:** SQLite (can be easily swapped with PostgreSQL or other databases)
- **Testing:** Unit tests and integration tests with 100% code coverage
- **CI/CD:** GitHub Actions for automated testing and linting
- **Cloud Hosting:** Deployed on[ PythonAnywhere](https://www.pythonanywhere.com/) (or any other cloud service)
- **Documentation:** Generated using Sphinx and hosted as a static site

**How to Run Locally**

Clone the repository: Then

cd todo

1\.

Set up a virtual environment:

python3 -m venv venv

source venv/bin/activate # On Windows use: venv\Scripts\activate

2\.

Install dependencies:

pip install -r requirements.txt

3\.

Apply database migrations:

python manage.py migrate

4\.

Create a superuser for the Django Admin panel:

python manage.py createsuperuser

5\.

Run the development server: python manage.py runserver

6\.

7\. Access the app in your browser at http://localhost:8000

**Testing**

Run unit tests and integration tests:

python manage.py test

●

**CI/CD Setup (GitHub Actions)**

The repository includes GitHub Actions for automating the following:

- Running tests (unit, integration, and E2E tests)
- Linting the code with **Flake8** and **Black**

**API Documentation**

The API endpoints can be tested using the provided **Postman Collection**. All CRUD operations for the tasks are included in the collection.

**Links:**

[https://sridhar100.pythonanywhere.com/ ](https://sridhar100.pythonanywhere.com/)<https://github.com/Sridhar144>
