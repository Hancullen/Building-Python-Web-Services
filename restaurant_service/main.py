from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from mockdbhelper import MockDBhelper as DBhelper
from user import User
from passwordhelper import PasswordHelper
import config
from bitlyhelper import BitlyHelper
import datetime
from forms import RegistrationForm

db = DBhelper()
PH = PasswordHelper()
BH = BitlyHelper()

app = Flask(__name__)
app.secret_key = b'\xff&\xa3\xc31\xaa\xd0#\xb68Kf\x8c\xf5\xfd@'
login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def home():
    registrationform = RegistrationForm()
    return render_template("home.html", registrationform=registrationform)

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

@app.route("/dashboard")
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = db.get_requests(current_user.get_id())
    for r in requests:
        deltaseconds = (now - r['time']).seconds
        r['waiting_in_minutes'] = "{}:{}".format(str(deltaseconds/60), str(deltaseconds % 60))
    return render_template("dashboard.html", requests=requests)

@app.route("/newrequest/<tid>")
def new_request(tid):
    db.add_request(tid, datetime.datetime.now())
    return "Your request has been received and a waiter will be with you shorly"

@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    db.delete_request(request_id)
    return redirect(url_for('dashboard'))

@app.route("/account")
@login_required
def account():
    tables = db.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    tablename = request.form.get("tablenumber")
    tableid = db.add_table(tablename, current_user.get_id())
    new_url = BH.shorten_url(config.base_url + "newrequest/" + tableid)
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)
