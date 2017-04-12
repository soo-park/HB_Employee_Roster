# -*- coding: utf-8 -*-
# Line one is necessary to have utf-8 recognized
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, request, flash, redirect,
                   session)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import func

import os
import datetime

# import employee related models
from model import Employee, Employee_company, Company, connect_to_db, db


## TODO: Build a function for importing Excel (below code imports one cell)
# def import_Excel():
#     import openpyxl
#     from openpyxl import load_workbook
#     wb = load_workbook(filename = 'static/doc/employee.xlsx')
#     sheet_ranges = wb['test'] #use the workbook tab name
#     print(sheet_ranges['A2'].value)


## TODO: Use regx to enforce formatting
    ## TODO: Build a function for importing Excel (below code imports one cell)
# def import_Excel():
#     """"""

#     # # make route
#     # # use function in route to call this function


#     # import openpyxl
#     # from openpyxl import load_workbook
#     # wb = load_workbook(filename = 'static/doc/employee.xlsx')
#     # sheet_ranges = wb['test'] #use the workbook tab name
#     # print(sheet_ranges['A2'].value)


def set_val_employee_id():
    """Set value for the next employee_id after seeding database"""

    # Get the Max employee_id in the database
    result = db.session.query(func.max(Employee.employee_id)).one()
    max_id = int(result[0])

    # Set the value for the next employee_id to be max_id + 1
    query = "SELECT setval('employees_employee_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    import_Excel()
    set_val_employee_id()


def get_map_from_sqlalchemy(a_object):
    """A SQLAlchemy utility to make a dictionary out of an object"""

    # this can be done at the front-end side using node.js and JS
    # if the programming was done at the front-end
    from sqlalchemy import inspect

    # A variable assigned to the SQLAlchemy object inspection
    inst = inspect(a_object)

    # this makes the result a map of all items in SQLAlchemy object
    obj_dic = inst.dict

    # A code to list all the attributes usable for the object
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]

    # To eliminate the object nodes and other magic nodes, each key gets
    # compared to the list of keys
    result = {}
    for item in obj_dic:
        if item in attr_names:
            result[item] = obj_dic[item]
        else:
            pass

    return result


def column_is_in_db(table, attr_name):
    """Check if a specific attribute name(column) is in a table"""

    # for item in Company.__dict__.iterkeys():
    #     print item
    # above code also prints the column

    return (attr_name in table.__dict__)


def value_is_same_as_db(table, attr_name, attr_value):
    """Check if a specific value of an attribute"""

    new_instance = table.query.filter_by(attr_name=attr_value)

    return table.query.filter_by(attr_name=attr_value).exists().scalar()


def column_exists_value_same(table, attr_name, attr_value):
    """Check if the column exists in the table and the value coming in is same"""

    return (column_is_in_db(table, attr_name) and 
            value_is_same_as_db(table, attr_name, attr_value))


# TODO: add a function to show if the employee has web access
# by calculating if the person has email and password.
# display that information only on admin side information page

# TODO: a function that counts empty space on database
# TODO: a function that allows you to fill in one space in database
# TODO: a function that generates log for the auto functions listed above
