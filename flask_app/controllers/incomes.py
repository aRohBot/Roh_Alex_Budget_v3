from flask_app import app
from flask_app.models.user import User
from flask_app.models.budget import Budget
from flask_app.models.income import Income
from flask_app.models.expense import Expense
from flask import request, render_template, session, redirect, flash, get_flashed_messages

@app.route('/create/income', methods=['POST'])
def create_income():
    if 'user_id' not in session:
        return redirect('/')
    if not Income.validate_income(request.form):
        return redirect('/dashboard')
    data={
        "company_name": request.form['company_name'],
        "monthly_payment": request.form['monthly_payment'],
        "budget_id": request.form['budget_id']
    }
    income_id=Income.save(data)
    budget_id=data['budget_id']
    return redirect(f'/view/budget/{budget_id}')

@app.route('/income/delete/<int:id>')
def destroy_income(id):
    budget_id=Income.get_by_id({'id':id}).budget_id
    Income.delete({"id": id})
    return redirect(f'/view/budget/{budget_id}')

@app.route('/income/edit/<int:id>')
def income_edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': session['user_id']
    }
    return render_template('incomeedit.html', user=User.get_by_id(data), income_messages=get_flashed_messages(category_filter=["income"]), income=Income.get_by_id({'id': id}), )

@app.route('/update/income/<int:id>', methods=['POST'])
def update_income(id):
    if 'user_id' not in session:
        return redirect('/')
    user_data={
        'id': session['user_id']
    }
    data={
        'id': id,
        'company_name': request.form['company_name'],
        'monthly_payment': request.form['monthly_payment']
    }
    income_id=Income.update(data)
    budget_id=Income.get_by_id({'id':id}).budget_id
    return redirect(f'/view/budget/{budget_id}')

