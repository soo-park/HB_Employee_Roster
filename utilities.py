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


def change_sql_sub_obj_into_dic(obj):
    """change sql sub object into a dictionary"""

    if obj:
        obj_info = obj.__dict__
        remove = []
        for key in obj_info:
            if str(key)[0] == '_':
                remove.append(key)
        for key in remove: del obj_info[key]

        return obj_info


def change_sql_obj_into_dic(obj):
    """Chandge sql object into a dictionary"""

    if obj:
        obj_info = obj[0].__dict__
        remove = []
        for key in obj_info:
            if str(key)[0] == '_':
                remove.append(key)
        for key in remove: del obj_info[key]

        return obj_info


def import_Excel_one_cell(file_path, tab, cell):
    """a function for importing one Excel cell"""

    import openpyxl
    from openpyxl import load_workbook
    wb = load_workbook(filename=file_path)
    sheet_ranges = wb[tab] #use the workbook tab name
    print(sheet_ranges[cell].value)
    del openpyxl


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result
