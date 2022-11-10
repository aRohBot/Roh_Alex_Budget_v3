from flask_app.config.mysqlconnection import connectToMySQL
from flask import request, render_template, session, redirect, flash
import re
from flask_app.models.budget import Budget

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z0-9]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

class User:
    db = "manager"
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.profile = []
        self.budgets = []

    @staticmethod
    def validate_user(userdata):
        is_valid = True
        all_users = User.get_all_users()
        if len(userdata['username']) < 3:
            is_valid = False
            flash("Username must be at least 3 characters long", 'reg')
        if not NAME_REGEX.match(userdata['username']):
            is_valid = False
            flash("Only letters and numbers are allowed in your name", 'reg')
        for user in all_users:
            if user.email == userdata['email']:
                is_valid= False
                flash("Account with this email address already exists", 'reg')
        if not EMAIL_REGEX.match(userdata['email']):
            is_valid = False
            flash("Invalid email address", 'reg')
        if len(userdata['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters long", 'reg')
        if userdata['password'] != userdata['cpass']:
            is_valid = False
            flash("Passwords do not match", 'reg')
        if not PASSWORD_REGEX.match(userdata['password']):
            is_valid = False
            flash("Password must contain at least 1 number and 1 uppercase letter", 'reg')
        return is_valid

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        all_users=[]
        for row in results:
            all_users.append(cls(row))
        return all_users

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one_with_budgets(cls,data):
        query = "SELECT * FROM users LEFT JOIN budgets ON budgets.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_user = cls(results[0])
        if results[0]['budgets.id'] == None:
            return this_user
        for row in results:
            budget_data={
                "id": row['budgets.id'],
                "month": row['month'],
                "year": row['year'],
                "created_at": row['budgets.created_at'],
                "updated_at": row['budgets.updated_at'],
                "user_id": row['user_id']
            }
            this_user.budgets.append(Budget(budget_data))
        return this_user