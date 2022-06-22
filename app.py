from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import List
from config import connection_string
import sys
import types
import os

# pip install psycopg2-binary if app.py errors on pyscopg2
# connection_string should be a valid db string; currently it lives in config.py

session_maker = sessionmaker(bind=create_engine(connection_string))


def generate_models(models_file_name: str):
    """
    Utilizes sqlacodegen tool to read the structure of an existing database
    and generates the appropriate SQLAlchemy model code, using the delcarative style if possible.
    https://pypi.org/project/sqlacodegen/
    """
    os.system(
        f"sqlacodegen {connection_string} --noviews --outfile {models_file_name}.py"
    )


def get_table_attr(table):
    """Returns table information."""
    with session_maker() as session:
        columns = session.query(table)
        print(columns.column_descriptions)


def get_all_tables() -> List:
    """Returns a list of all tables from the database."""
    tables = metadata.tables.keys()
    _tables = []  # Lazy list

    for _table in tables:
        _tables.append(_table)

    return _tables


def get_classes():
    """Returns a list of code model objects"""
    import models
    from inspect import isclass

    classes = [x for x in dir(models) if isclass(getattr(models, x))]
    print(classes[1:])

    return classes[1:]


def str_to_class(field: str):
    try:
        identifier = getattr(sys.modules[__name__], field)
    except AttributeError:
        raise NameError("%s doesn't exist." % field)
    if isinstance(identifier, (type)):
        print(field + " class found.")
        return identifier
    raise TypeError("%s is not a class." % field)


def create_table_repr(table: Base.metadata):
    """
    Writes a __repr__ dunder method to add to DB models.
    This will help with string representation of returned information.
    """
    attrs = table.__table__.columns.keys()

    with open(f"repr\__repr__.py", "a") as f:

        f.write("def __repr__(self):\n")  # This writes the function def
        f.write(
            f"    {table.__table__.name} = " + "{\n"
        )  # This writes the table name, and the starting curly brackets

        print(
            "------------------------------------------------------------------\n"
            + table.__table__.name
            +"\n------------------------------------------------------------------"
        )

        for attr in attrs:
            print(f'"{attr}": self.{attr},')
            f.write(f'        "{attr}": self.{attr},\n')

        f.write("        }\n" + f"    return str(dict({table.__table__.name}))")
        f.write("\n")
        f.write("\n")


def create_all_tables_repr():

    classes = get_classes()
    output_classes = list(map(str_to_class, classes))

    for table in output_classes:
        try:
            create_table_repr(table)  # append the repr to file
            print(
                f"Created __repr__ for table {table}\n",
                "-----------------------------------------------------------------\n",
            )
        except Exception:
            print("Error in create_all_table_repr")


def get_company_users(company_id):
    """Example usage of ORM querying a User table based on a company ID"""
    with session_maker() as session:
        user_records = (
            session.query(User, Relationship)
            .filter(User.id == Relationship.user_id)
            .where(Relationship.company_id == company_id)
            .all()
        )

        for user, relationship in user_records:
            print(f"Name : {user.name}\n" + f"Company ID: {relationship.company_id}\n")

    return user_records


# generate_models('test')
# get_table_attr(User)
# print(get_all_tables())
# print(type(User))
# create_table_repr(User)

# create_all_tables_repr()

# get_company_users(18)

# classes = get_classes()
# print(type(classes))

# str_to_class('User')

create_all_tables_repr()
