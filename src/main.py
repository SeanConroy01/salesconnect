import os
from flask import Flask, redirect, render_template, url_for, request, flash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from models import Customer
from forms import CreateCustomerForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

## Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


db.create_all()

@app.route('/')
def home():
   return render_template("index.html", title="Home")

@app.route('/customer')
def get_customers():
  customers = Customer.query.all()
  return render_template("customers.html", title="Customers", customers=customers)

@app.route("/customer/<int:customer_id>", methods=["GET"])
def show_customer(customer_id):
  requested_customer = Customer.query.get(customer_id)
  return render_template("customer.html", title=requested_customer.name, customer=requested_customer)

@app.route("/new-customer", methods=["GET", "POST"])
def new_customer():
  form = CreateCustomerForm()
  if form.validate_on_submit():
    new_customer = Customer(
      name=form.name.data,
      industry=form.industry.data,
      date=date.today().strftime("%B %d, %Y")
    )
    db.session.add(new_customer)
    db.session.commit()
    flash("Customer has been Created.", "success")
    return redirect(url_for("get_customers"))
  return render_template("make-customer.html", title="New Customers", form=form)

@app.route("/edit-customer/<int:customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
  customer = Customer.query.get(customer_id)
  edit_form = CreateCustomerForm(
    name=customer.name,
    industry=customer.industry,
  )
  if edit_form.validate_on_submit():
    customer.name = edit_form.name.data
    customer.industry = edit_form.industry.data
    db.session.commit()
    flash("Customer has been updated.", "success")
    return redirect(url_for("show_customer", customer_id=customer.id))

  return render_template("make-customer.html", title="Edit Customers", form=edit_form, is_edit=True, customer_id=customer_id)

@app.route("/delete/<int:customer_id>", methods=["GET"])
def delete_customer(customer_id):
  customer_to_delete = Customer.query.get(customer_id)
  db.session.delete(customer_to_delete)
  db.session.commit()
  flash("Customer has been delelted.", "danger")
  return redirect(url_for('get_customers'))

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