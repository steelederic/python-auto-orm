from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import List, Tuple
from config import connection_string
import sys
import types


# pip install psycopg2-binary if app.py errors on pyscopg2

# Used with context manager to create a session with the db
session_maker = sessionmaker(bind=create_engine(connection_string))

###################################################
#    TO GENERATE MODELS, RUN CREATE_MODELS.PY     #
###################################################


def get_table_attr(table) -> List[str]:
    """Returns table information."""
    with session_maker() as session:
        columns = session.query(table)
        print(columns.column_descriptions)

    return [col for col in columns]


def get_all_tables() -> List[str]:
    """Returns a list of all tables from the database."""
    tables = metadata.tables.keys()

    return [table for table in tables]

def get_classes() -> List[object]:
    """Returns a list of code model objects"""
    import models
    from inspect import isclass

    return [x for x in dir(models) if isclass(getattr(models, x))][1:]


def str_to_class(field: str):
    """Returns a class object type from a string input. Example : <class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>"""
    try:
        identifier = getattr(sys.modules[__name__], field)
    except AttributeError:
        raise NameError("%s doesn't exist." % field)
    if isinstance(identifier, (type)):
        print(field + " class found.")
        return identifier
    raise TypeError("%s is not a class." % field)


def create_table_repr(table) -> None:
    """
    Writes a __repr__ dunder method to add to DB models.
    This will help with string representation of returned information.
    """
    attrs = table.__table__.columns.keys()

    with open(f"__repr__.py", "a") as f:

        f.write("def __repr__(self):\n")  # This writes the function def
        f.write(
            f"    {table.__table__.name} = " + "{\n"
        )  # This writes the table name, and the starting curly brackets

        print(
            "------------------------------------------------------------------\n"
            + table.__table__.name
            + "\n------------------------------------------------------------------"
        )

        for attr in attrs:
            print(f'"{attr}": self.{attr},')
            f.write(f'        "{attr}": self.{attr},\n')

        f.write("        }\n" + f"    return str(dict({table.__table__.name}))")
        f.write("\n")
        f.write("\n")


def create_all_tables_repr() -> None:
    """Given models.py iterate over every table class and generate/write a __repr__ method to __repr__.py"""

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


def get_company_users(company_id) -> List[Tuple[str,str]]:
    """Example usage of ORM querying a User table based on a company ID"""
    with session_maker() as session:
        user_records = (
            session.query(User, Relationship)
            .filter(User.id == Relationship.user_id)
            .where(Relationship.company_id == company_id)
            .all()
        )
    return [(x.name, y.company_id) for x, y in user_records]
