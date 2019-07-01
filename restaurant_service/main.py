from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from mockdbhelper import MockDBhelper as DBhelper
from user import User
from passwordhelper import PasswordHelper
import config
from bitlyhelper import BitlyHelper
import datetime
from forms import CreateTableForm, RegistrationForm, LoginForm
from flask_wtf.csrf import CSRFProtect

db = DBhelper()
PH = PasswordHelper()
BH = BitlyHelper()

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b'\xff&\xa3\xc31\xaa\xd0#\xb68Kf\x8c\xf5\xfd@'
login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def home():
    registrationform = RegistrationForm()
    loginform = LoginForm()
    return render_template("home.html", loginform=loginform, registrationform=registrationform)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        stored_user = db.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data, stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('account'))
            # return account()
        form.loginemail.errors.append('Email or Password Invalid')
    return render_template('home.html', loginform=form, registrationform=RegistrationForm())

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/register", methods=["POST", "GET"])
def register():
    #update version using registration form
    form = RegistrationForm()
    if form.validate_on_submit():
        if db.get_user(form.email.data):
            form.email.errors.append('Your email is already registered')
            return render_template('home.html', registrationform=form, loginform=LoginForm())
    #Old version to compare
    # pw1 = request.form.get("password")
    # confirmed_pw = request.form.get("password2")
    # if not pw1 == confirmed_pw:
    #     return redirect(url_for('home'))
    # if db.get_user(email): #verify if user's email already exists
    #     return redirect(url_for('home'))
        hashed = PH.get_hash(form.password2.data)
        db.add_user(form.email.data, hashed)
        # return redirect(url_for('home'))
        return render_template('home.html', loginform=LoginForm(), registrationform=form, onloadmessage='Registration successful. Please log in.')
    return render_template('home.html', loginform=LoginForm(), registrationform=form)

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
    return render_template("account.html", tables=tables, createtable=CreateTableForm())

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    form = CreateTableForm()
    if form.validate_on_submit():
        tableid = db.add_table(form.tablenumber.data, current_user.get_id())
        new_url = BH.shorten_url(config.base_url + "newrequest/" + tableid)
        db.update_table(tableid, new_url)
        return redirect(url_for('account'))
    return render_template('account.html', createtable=form, tables=db.get_tables(current_user.get_id()))

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
