from flask_app.controllers import users, budgets, incomes, expenses

from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)
