from flask_app import app
from flask_app.models.user import User
from flask_app.models.budget import Budget
from flask import request, render_template, session, redirect, flash, get_flashed_messages
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login_registration.html', reg_messages=get_flashed_messages(category_filter=["reg"]), log_messages=get_flashed_messages(category_filter=["login"]))

@app.route('/register', methods=["POST"])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    data={
        "username": request.form['username'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id=User.create(data)
    session['user_id']=user_id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_one_with_budgets(data))

@app.route('/login', methods=["POST"])
def login():
    this_user=User.get_user_by_email({'email': request.form['email']})
    if this_user:
        if bcrypt.check_password_hash(this_user.password, request.form['password']):
            session['user_id'] = this_user.id
            return redirect('/dashboard')
    flash("Invalid Email /Password combination, Try again", 'login')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')