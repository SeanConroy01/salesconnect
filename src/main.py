import os
from flask import Flask, redirect, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from models import db, User
from forms import RegisterForm, LoginForm, ChangePasswordForm
from routes.customer import customer_routes

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

## Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
  return redirect(url_for("login"))

db.create_all()

@app.route('/')
@login_required
def home():
   return render_template("index.html", title="Home")

app.register_blueprint(customer_routes)

@app.route('/create-user', methods=["GET", "POST"])
def new_user():
  form = RegisterForm()
  if form.validate_on_submit():
    if User.query.filter_by(email=form.email.data).first():
      flash("The email address provided is already associated with another account, Please login or try a different email address.", "danger")
      return redirect(url_for('new_user'))
    else:
      hash_and_salted_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
      new_user = User(name=form.name.data, email=form.email.data, role=form.role.data, password=hash_and_salted_password)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for("admin_panel"))
  else:
    return render_template("make-user.html", form=form, title="Sign Up")

# Login
@app.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=request.form['email']).first()
    if not user or not check_password_hash(user.password, form.password.data):
      flash("The name or password provided were incorrect, please try again.", "danger")
      return redirect(url_for('login'))
    else:
      login_user(user)
      return redirect(url_for("home"))
  else:
    return render_template("login.html", form=form, title="Login")

# Change Password
@app.route('/change-password', methods=["GET", "POST"])
@login_required
def change_password():
  form = ChangePasswordForm()
  if form.validate_on_submit():
    if not check_password_hash(current_user.password, form.current_password.data):
      flash("The current password is incorrect, please try again.", "danger")
      return redirect(url_for('change_password'))
    elif form.new_password.data != form.confirm_password.data:
      flash("The new password and confirmation password provided do not match, please try again.", "danger")
      return redirect(url_for('change_password'))
    else:
      user = User.query.get(current_user.id)
      user.password=generate_password_hash(form.new_password.data, method='pbkdf2:sha256', salt_length=8)
      db.session.commit()
      flash("Your password has been changed.", "success")
      return redirect(url_for("home"))
  else:
    return render_template("change-password.html", form=form, title="Change Password")

# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin-panel')
@login_required
def admin_panel():
    users = User.query.all()
    return render_template("admin-panel.html", title="Admin Panel", all_users=users, current_user=current_user)

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
 return render_template('errors/404.html', title="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
  return render_template('errors/500.html', title="Something Went Wrong"), 500

@app.errorhandler(403)
def page_forbidden(e):
  return redirect('/')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, port=os.getenv('PORT'))