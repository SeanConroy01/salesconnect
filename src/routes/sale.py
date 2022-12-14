from datetime import date
from flask import render_template, redirect, flash, url_for, Blueprint
from flask_login import login_required, current_user
from src.forms import CreateSaleForm
from src.main import db, Sale, Customer, User
from src.common import get_related_sales, admin_only

sale_routes = Blueprint('sale', __name__, template_folder='templates')

# Sale - Show Sales
@sale_routes.route('/sale')
@login_required
def get_sales():
  return render_template("sales.html", title="Customers", sales=get_related_sales(current_user))

# Sale - New Sale
@sale_routes.route("/new-sale/<int:customer_id>", methods=["GET", "POST"])
@login_required
def new_sale(customer_id):
  # Create form
  form = CreateSaleForm()
  if form.validate_on_submit():
    # Create new sale object
    new_sale = Sale(
      value=form.value.data,
      status=form.status.data,
      parent_customer=Customer.query.get(customer_id),
      rep=User.query.get(current_user.id),
      date=date.today().strftime("%B %d, %Y")
    )
    # save new object
    db.session.add(new_sale)
    db.session.commit()
    # Log essage to user
    flash("Sale has been Created.", "success")
    return redirect(url_for("customer.show_customer", customer_id=customer_id))
  else:
    # Log error essage to user
    if form.errors:
        for error in form.errors.values():
          flash(error[0], "danger")
    return render_template("make-sale.html", title="New Sale", customer_id=customer_id, form=form,  current_user=current_user)

# Sale - Edit Sale
@sale_routes.route("/edit-sale/<int:sale_id>", methods=["GET", "POST"])
@login_required
def edit_sale(sale_id):
  sale = Sale.query.get(sale_id)
  # Create form
  edit_form = CreateSaleForm(
    value=sale.value
  )
  # Update sale data
  if edit_form.validate_on_submit():
    sale.value = edit_form.value.data
    sale.status = edit_form.status.data
    sale.date = date.today().strftime("%B %d, %Y")
    db.session.commit()
    # Log essage to user
    flash("Sale has been updated.", "success")
    return redirect(url_for("customer.show_customer", customer_id=sale.customer_id))
  else:
    # Log error essage to user
    if edit_form.errors:
        for error in edit_form.errors.values():
          flash(error[0], "danger")
    return render_template("make-sale.html", title="Edit Contact", form=edit_form, is_edit=True, sale_id=sale.id)

# Sale - Delete Sale
@sale_routes.route("/delete-sale/<int:sale_id>", methods=["GET"])
@login_required
@admin_only
def delete_sale(sale_id):
  # Get sale to delete
  sale_to_delete = Sale.query.get(sale_id)
  to_return = sale_to_delete.customer_id
  # Delete sale
  db.session.delete(sale_to_delete)
  db.session.commit()
  # Log essage to user
  flash("Sale has been deleted.", "danger")
  return redirect(url_for('customer.show_customer', customer_id=to_return))
