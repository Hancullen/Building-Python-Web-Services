from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from mockdbhelper import MockDBhelper as DBhelper
from user import User
from passwordhelper import PasswordHelper
import config
from bitlyhelper import BitlyHelper

db = DBhelper()
PH = PasswordHelper()
BH = BitlyHelper()

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
    tables = db.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)

@app.route("/dashboard")
@login_required
def dashboard():
  return render_template("dashboard.html")

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    tablename = request.form.get("tablenumber")
    tableid = db.add_table(tablename, current_user.get_id())
    new_url = config.base_url + "newrequest/" + tableid
    db.update_table(tableid, new_url)
    return redirect(url_for('account'))

@app.route("/account/deletetable")
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    db.delete_table(tableid)
    return redirect(url_for('account'))

@login_manager.user_loader
def load_user(user_id):
    user_password = db.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route("/login", methods=["POST", "GET"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = db.get_user(email)
    if stored_user and PH.validate_password(password, stored_user['hashed']):
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
    email = request.form.get("email")
    pw1 = request.form.get("password")
    confirmed_pw = request.form.get("password2")
    if not pw1 == confirmed_pw:
        return redirect(url_for('home'))
    if db.get_user(email): #verify if user's email already exists
        return redirect(url_for('home'))
    hashed = PH.get_hash(pw1)
    db.add_user(email, hashed)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
