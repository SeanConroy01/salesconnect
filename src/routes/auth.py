from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, redirect, flash, url_for, Blueprint, request, abort
from flask_login import login_required

from src.forms import RegisterForm, LoginForm, ChangePasswordForm
from src.main import db, User
from src.common import admin_only

auth_routes = Blueprint('auth', __name__, template_folder='templates')

# Authentication - Create User
@auth_routes.route('/create-user', methods=["GET", "POST"])
@login_required
@admin_only
def new_user():
  form = RegisterForm()
  if form.validate_on_submit():
    if User.query.filter_by(email=form.email.data).first():
      flash("The email address provided is already associated with another account, Please login or try a different email address.", "danger")
      return redirect(url_for('auth.new_user'))
    else:
      hash_and_salted_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
      new_user = User(name=form.name.data, email=form.email.data, role=form.role.data, password=hash_and_salted_password)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for("auth.admin_panel"))
  else:
    if form.errors:
      for error in form.errors.values():
        flash(error[0], "danger")
    return render_template("make-user.html", form=form, title="Sign Up")

# Authentication - Delete User
@auth_routes.route("/delete-user/<int:user_id>", methods=["GET"])
@login_required
@admin_only
def delete_user(user_id):
  user_to_delete = User.query.get(user_id)
  # Delete links sales
  for sale in user_to_delete.sales:
    db.session.delete(sale)
  db.session.delete(user_to_delete)
  db.session.commit()
  flash("User has been deleted.", "danger")
  return redirect(url_for('auth.admin_panel'))

# Authentication - Login
@auth_routes.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=request.form['email'].lower()).first()
    if not user or not check_password_hash(user.password, form.password.data):
      flash("The name or password provided were incorrect, please try again.", "danger")
      return redirect(url_for('auth.login'))
    else:
      login_user(user)
      return redirect(url_for("home.home"))
  else:
    return render_template("login.html", form=form, title="Login")

# Authentication - Change Password
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
      return redirect(url_for("home.home"))
  else:
    return render_template("change-password.html", form=form, title="Change Password")

# Authentication - Logout
@auth_routes.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

# Authentication - Admin Panel
@auth_routes.route('/admin-panel')
@login_required
@admin_only
def admin_panel():
  users = User.query.all()
  return render_template("admin-panel.html", title="Admin Panel", num_user=len(users), all_users=users, current_user=current_user)

# Authentication - Create Default User
@auth_routes.route('/create-admin')
def create_admin():
  if len(User.query.all()) == 0:
    hash_and_salted_password = generate_password_hash("1234567890", method='pbkdf2:sha256', salt_length=8)
    new_user = User(name="Admin", email="admin@cisco.com", role="admin", password=hash_and_salted_password)
    db.session.add(new_user)
    db.session.commit()
    hash_and_salted_password = generate_password_hash("1234567890", method='pbkdf2:sha256', salt_length=8)
    new_user = User(name="User", email="user@cisco.com", role="user", password=hash_and_salted_password)
    db.session.add(new_user)
    db.session.commit()
  return redirect(url_for('home.home'))
