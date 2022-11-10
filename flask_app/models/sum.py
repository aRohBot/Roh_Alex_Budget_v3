from flask_app.config.mysqlconnection import connectToMySQL
from flask import request, render_template, session, redirect, flash


class Sum:
    db = "manager"
    def __init__(self, data):
        self.id = data['id']
        self.sum = data['sum']