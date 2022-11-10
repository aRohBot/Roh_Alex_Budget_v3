from flask_app import app
from flask_app.models.user import User
from flask_app.models.budget import Budget
from flask import request, render_template, session, redirect, flash, get_flashed_messages

@app.route('/budget')
def budget_form():
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': session['user_id']
    }
    return render_template('budgetform.html', user=User.get_by_id(data), budget_messages=get_flashed_messages(category_filter=["budget"]))

@app.route('/create/budget', methods=['POST'])
def create_budget():
    if 'user_id' not in session:
        return redirect('/')
    data={
        'month': request.form['month'],
        'year': request.form['year'],
        'user_id': session['user_id']
    }
    budget_id=Budget.save_budget(data)
    return redirect(f'/view/budget/{budget_id}')

@app.route('/budget/delete/<int:id>')
def destroy_budget(id):
    Budget.delete({"id": id})
    return redirect('/dashboard')

@app.route('/budget/edit/<int:id>')
def budget_edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': session['user_id']
    }
    return render_template('budgetedit.html', user=User.get_by_id(data), budget=Budget.get_by_id({'id':id}), budget_messages=get_flashed_messages(category_filter=["budget"]))

@app.route('/update/budget/<int:id>', methods=['POST'])
def update_budget(id):
    if 'user_id' not in session:
        return redirect('/')
    user_data={
        'id': session['user_id']
    }
    data={
        'id': id,
        'month': request.form['month'],
        'year': request.form['year'],
        'user_id': request.form['user_id']
    }
    budget_id=Budget.update(data)
    return redirect(f'/view/budget/{id}')

@app.route('/view/budget/<int:id>')
def budget_details(id):
    if 'user_id' not in session:
        return redirect('/')
    user_data={
        'id': session['user_id']
    }
    budget_data={
        'id': id
    }
    return render_template('view_budget.html', user=User.get_by_id(user_data), budget=Budget.get_one_with_incomes(budget_data), expenses=Budget.get_one_with_expenses(budget_data), expense_sum=Budget.sum_of_expenses(budget_data), income_sum=Budget.sum_of_income(budget_data))