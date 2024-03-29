# chatBot-assignment
Create a Virtual Environment
```python -m venv env```
Activate the Virtual Environment
```cd env/Scripts/activate```
Install Project Dependencies
```pip install -r requirements.txt```
Navigate to the Project Directory
```cd <main_project_name>```
run the migrations
```python manage.py makemigrations <app_name>```
```python manage.py migrate```
Run the created project
```python manage.py runserver```
then go to swagger docs:
```http://localhost:8000/api/docs```
