from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, redirect, flash, url_for, Blueprint, request
from flask_login import login_required
from forms import RegisterForm, LoginForm, ChangePasswordForm
from models import db, User

auth_routes = Blueprint('auth', __name__, template_folder='templates')

@auth_routes.route('/create-user', methods=["GET", "POST"])
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
      return redirect(url_for("auth.admin_panel"))
  else:
    return render_template("make-user.html", form=form, title="Sign Up")

# Login
@auth_routes.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=request.form['email']).first()
    if not user or not check_password_hash(user.password, form.password.data):
      flash("The name or password provided were incorrect, please try again.", "danger")
      return redirect(url_for('login'))
    else:
      login_user(user)
      return redirect(url_for("home.home"))
  else:
    return render_template("login.html", form=form, title="Login")

# Change Password
@auth_routes.route('/change-password', methods=["GET", "POST"])
@login_required
def change_password():
  form = ChangePasswordForm()
  if form.validate_on_submit():
    if not check_password_hash(current_user.password, form.current_password.data):
      flash("The current password is incorrect, please try again.", "danger")
      return redirect(url_for('change_password'))
    elif form.new_password.data != form.confirm_password.data:
      flash("The new password and confirmation password provided do not match, please try again.", "danger")
      return redirect(url_for('auth.change_password'))
    else:
      user = User.query.get(current_user.id)
      user.password=generate_password_hash(form.new_password.data, method='pbkdf2:sha256', salt_length=8)
      db.session.commit()
      flash("Your password has been changed.", "success")
      return redirect(url_for("heom.home"))
  else:
    return render_template("change-password.html", form=form, title="Change Password")

# Logout
@auth_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_routes.route('/admin-panel')
@login_required
def admin_panel():
    users = User.query.all()
    return render_template("admin-panel.html", title="Admin Panel", all_users=users, current_user=current_user)
