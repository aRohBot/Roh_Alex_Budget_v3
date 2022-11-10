from flask_app import app
from flask_app.models.user import User
from flask_app.models.budget import Budget
from flask_app.models.income import Income
from flask_app.models.expense import Expense
from flask import request, render_template, session, redirect, flash, get_flashed_messages

@app.route('/create/expense', methods=['POST'])
def create_expense():
    if 'user_id' not in session:
        return redirect('/')
    if not Expense.validate_expense(request.form):
        return redirect('/dashboard')
    data={
        "name": request.form['name'],
        "description": request.form['description'],
        "cost": request.form['cost'],
        "budget_id": request.form['budget_id']
    }
    expense_id=Expense.save(data)
    budget_id=data['budget_id']
    return redirect(f'/view/budget/{budget_id}')

@app.route('/expense/delete/<int:id>')
def destroy_expense(id):
    budget_id=Expense.get_by_id({'id':id}).budget_id
    Expense.delete({"id": id})
    return redirect(f'/view/budget/{budget_id}')

@app.route('/expense/edit/<int:id>')
def expense_edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': session['user_id']
    }
    return render_template('expenseedit.html', user=User.get_by_id(data), expense_messages=get_flashed_messages(category_filter=["expense"]), expense=Expense.get_by_id({'id': id}))

@app.route('/update/expense/<int:id>', methods=['POST'])
def update_expense(id):
    if 'user_id' not in session:
        return redirect('/')
    user_data={
        'id': session['user_id']
    }
    data={
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'cost': request.form['cost']
    }
    expense_id=Expense.update(data)
    budget_id=Expense.get_by_id({'id':id}).budget_id
    return redirect(f'/view/budget/{budget_id}')