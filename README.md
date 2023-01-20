# python-auto-orm
```
Given a DB connection string, automatically produce table model code to be used with SQLAlchemy ORM.
Optionally, produce __repr__ dunder methods for each class to help represent each class as a string

Currently only supports postgresql.
```
# To Install
```
With Python 3 installed:
Clone Repo
Create a virtual environment
pip install -r requirements.txt
run create_models.py with a DB connection string to generate model code
run app.py
```
