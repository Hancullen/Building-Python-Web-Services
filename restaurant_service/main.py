from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from mockdbhelper import MockDBhelper as DBhelper
from user import User
from passwordhlper import PasswordHelper

db = DBhelper()
PH = PasswordHelper()
app = Flask(__name__)
app.secret_key = b'\xff&\xa3\xc31\xaa\xd0#\xb68Kf\x8c\xf5\xfd@'
login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account")
@login_required
def account():
    return "You are logged in"

@login_manager.user_loader
def load_user(user_id):
    user_password = db.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route("/login", methods=["POST", "GET"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_password = db.get_user(email)
    if user_password and user_password == password:
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
        # return account()
    return home()

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/register", methods=["POST", "GET"])
def register():
    email = request.from.get("email")
    pw1 = request.form.get("password")
    confirmed_pw = request.form.get("password2")
    if not pw1 = confirmed_pw:
        return redirect(url_for('home'))
    if db.get_user(email): #verify if user's email already exists
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
