from flask_app.config.mysqlconnection import connectToMySQL
from flask import request, render_template, session, redirect, flash
import re
import flask_app.models.user as user

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class Profile:
    db = "manager"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = user.User.get_by_id({'id': data['user_id']})

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, user_id) VALUES (%(first_name)s, %(last_name)s, %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    @staticmethod
    def validate_user(userdata):
        is_valid = True
        if len(userdata['first_name']) < 3:
            is_valid = False
            flash("First name must be at least 3 characters long", 'profile')
        if len(userdata['last_name']) < 3:
            is_valid = False
            flash("Last name must be at least 3 characters long", 'profile')
        if not NAME_REGEX.match(userdata['first_name']):
            is_valid = False
            flash("Only letters are allowed in your name", 'profile')
        if not NAME_REGEX.match(userdata['last_name']):
            is_valid = False
            flash("Only letters are allowed in your name", 'profile')
        return is_valid