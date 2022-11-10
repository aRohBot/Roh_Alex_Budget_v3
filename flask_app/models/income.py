from flask_app.config.mysqlconnection import connectToMySQL
from flask import request, render_template, session, redirect, flash
import flask_app.models.budget as budget
import re

class Income:
    db = "manager"
    def __init__(self, data):
        self.id = data['id']
        self.company_name = data['company_name']
        self.monthly_payment = data['monthly_payment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.budget_id = data['budget_id']


    @staticmethod
    def validate_income(userdata):
        is_valid = True
        if len(userdata['company_name'])<2:
            is_valid=False
            flash("Name must be at least 2 characters long", 'expense')
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM incomes;"
        results = connectToMySQL(cls.db).query_db(query)
        all_incomes = []
        for row in results:
            all_incomes.append(cls(row))
        return all_incomes

    @classmethod
    def save(cls,data):
        query = "INSERT INTO incomes (company_name, monthly_payment, budget_id) VALUES (%(company_name)s, %(monthly_payment)s, %(budget_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM incomes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE incomes SET company_name = %(company_name)s, monthly_payment = %(monthly_payment)s WHERE incomes.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM incomes WHERE incomes.id= %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return
