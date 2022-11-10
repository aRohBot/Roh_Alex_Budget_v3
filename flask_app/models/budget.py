from flask_app.config.mysqlconnection import connectToMySQL
from flask import request, render_template, session, redirect, flash
import flask_app.models.user as user
from flask_app.models.income import Income
from flask_app.models.expense import Expense
from flask_app.models.sum import Sum
import re

YEAR_REGEX = re.compile(r'^[0-9]+$')

class Budget:
    db = "manager"
    def __init__(self, data):
        self.id = data['id']
        self.month = data['month']
        self.year = data['year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = user.User.get_by_id({'id':session['user_id']})
        self.expenses =[]
        self.incomes =[]
        self.sum = 0


    @staticmethod
    def validate_budget(userdata):
        is_valid = True
        if len(userdata['month'])<3:
            is_valid=False
            flash("Month must be at least 3 characters long", 'budget')
        if len(userdata['year'])<4:
            is_valid=False
            flash("Year must be at least 4 characters long", 'budget')
        if not YEAR_REGEX.match(userdata['year']):
            is_valid = False
            flash("Only numbers are allowed", 'budget')
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM budgets;"
        results = connectToMySQL(cls.db).query_db(query)
        all_budgets = []
        for row in results:
            all_budgets.append(cls(row))
        return all_budgets

    @classmethod
    def save_budget(cls,data):
        query = "INSERT INTO budgets (month, year, user_id) VALUES (%(month)s, %(year)s, %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM budgets WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE budgets SET month = %(month)s, year = %(year)s WHERE budgets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM budgets WHERE budgets.id= %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def get_one_with_incomes(cls,data):
        query = "SELECT * FROM budgets LEFT JOIN incomes ON incomes.budget_id = budgets.id WHERE budgets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_budget = cls(results[0])
        if results[0]['incomes.id'] == None:
            return this_budget
        for row in results:
            income_data={
                "id": row['incomes.id'],
                "company_name": row['company_name'],
                "monthly_payment": row['monthly_payment'],
                "created_at": row['incomes.created_at'],
                "updated_at": row['incomes.updated_at'],
                "budget_id": row['budget_id']
            }
            this_budget.incomes.append(Income(income_data))
        return this_budget

    @classmethod
    def get_one_with_expenses(cls,data):
        query = "SELECT * FROM budgets LEFT JOIN expenses ON expenses.budget_id = budgets.id WHERE budgets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_budget = cls(results[0])
        if results[0]['expenses.id'] == None:
            return this_budget
        for row in results:
            expense_data={
                "id": row['expenses.id'],
                "name": row['name'],
                "description": row['description'],
                "cost": row['cost'],
                "created_at": row['expenses.created_at'],
                "updated_at": row['expenses.updated_at'],
                "budget_id": row['budget_id']
            }
            this_budget.expenses.append(Expense(expense_data))
        return this_budget

    @classmethod
    def sum_of_expenses(cls,data):
        query = "SELECT *, SUM(cost) AS sum FROM budgets LEFT JOIN expenses ON expenses.budget_id = budgets.id WHERE budgets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results[0]['sum']== None:
            sum = Sum({'id':id, 'sum': 0})
            return sum
        for row in results:
            esum_data ={
                'id': id,
                'sum': row['sum']
            }
            sum = Sum(esum_data)
        return sum

    @classmethod
    def sum_of_income(cls,data):
        query = "SELECT *, SUM(monthly_payment) AS sum FROM budgets LEFT JOIN incomes ON incomes.budget_id = budgets.id WHERE budgets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results[0]['sum']== None:
            sum = Sum({'id':id, 'sum': 0})
            return sum
        for row in results:
            isum_data ={
                'id': id,
                'sum': row['sum']
            }
            isum = Sum(isum_data)
        return isum

    @classmethod
    def get_one_with_expenses_incomes(cls,data):
        query = "SELECT * FROM budgets LEFT JOIN expenses ON expenses.budget_id = budgets.id LEFT JOIN incomes ON incomes.budget_id = expenses.budget_id WHERE budgets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_budget = cls(results[0])
        if 'expenses.id' not in results[0]:
            return this_budget
        for row in results:
            expense_data={
                "id": row['expenses.id'],
                "name": row['name'],
                "description": row['description'],
                "cost": row['cost'],
                "created_at": row['expenses.created_at'],
                "updated_at": row['expenses.updated_at'],
                "budget_id": row['budget_id']
            }
            income_data={
                "id": row['incomes.id'],
                "company_name": row['company_name'],
                "monthly_payment": row['monthly_payment'],
                "created_at": row['incomes.created_at'],
                "updated_at": row['incomes.updated_at'],
                "budget_id": row['budget_id']
            }
            this_budget.expenses.append(Expense(expense_data))
            this_budget.incomes.append(Income(income_data))
        return this_budget