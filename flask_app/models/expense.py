from flask_app.config.mysqlconnection import connectToMySQL
from flask import request, render_template, session, redirect, flash
import flask_app.models.budget as budget
import re


class Expense:
    db = "manager"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.cost = data['cost']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.budget_id = data['budget_id']


    @staticmethod
    def validate_expense(userdata):
        is_valid = True
        if len(userdata['name'])<2:
            is_valid=False
            flash("Name must be at least 2 characters long", 'expense')
        if len(userdata['description'])<4:
            is_valid=False
            flash("Description must be at least 4 characters long", 'expense')
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM expenses;"
        results = connectToMySQL(cls.db).query_db(query)
        all_expenses = []
        for row in results:
            all_expenses.append(cls(row))
        return all_expenses

    @classmethod
    def save(cls,data):
        query = "INSERT INTO expenses (name, description, cost, budget_id) VALUES (%(name)s, %(description)s, %(cost)s, %(budget_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM expenses WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE expenses SET name = %(name)s, description = %(description)s, cost = %(cost)s WHERE expenses.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM expenses WHERE expenses.id= %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

