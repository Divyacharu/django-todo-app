# Django Todo Management App

A simple **Todo Management App** built using Django for managing project tasks.  
It supports task creation, completion, deletion, and exporting summaries as GitHub Gists.  

## Features
- Add, complete, and remove todos  
- Export project summaries as **GitHub Gists & local Markdown files**  
- Securely manage API tokens using environment variables  

---


##  Setup Instructions


###  Clone the Repository
```sh
git clone https://github.com/Divyacharu/django-todo-app.git`
cd django-todo-app\todo_project
```
# Set Up a Virtual Environment
```sh
python -m venv venv

venv\Scripts\activate
```

### install dependencies
```sh
pip install -r requirements.txt
```

### Configure Environment Variables
To securely use the GitHub Token, set up an environment variable:
```sh
set GITHUB_TOKEN=your_personal_access_token

```
### Run Database Migrations
```sh
python manage.py migrate
```
### Create a Superuser (For Admin Access)
```sh
python manage.py createsuperuser
```
### Start the Development Server
```sh
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.