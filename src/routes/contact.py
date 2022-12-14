from flask import render_template, redirect, flash, url_for, Blueprint
from flask_login import login_required

from src.forms import CreateContactForm
from src.main import db, Contact, Customer
from src.common import admin_only

contact_routes = Blueprint('contact', __name__, template_folder='templates')

# Contact - New Contact
@contact_routes.route("/new-contact/<int:customer_id>", methods=["GET", "POST"])
@login_required
def new_contact(customer_id):
  # Create form
  form = CreateContactForm()
  if form.validate_on_submit():
    # Create new contact object
    new_customer = Contact(
      name=form.name.data,
      role=form.role.data,
      email=form.email.data.lower(),
      phone=form.phone.data,
      parent_customer=Customer.query.get(customer_id)
    )
    # Save new contact
    db.session.add(new_customer)
    db.session.commit()
    # Log message to user
    flash("Contact has been Created.", "success")
    return redirect(url_for("customer.show_customer", customer_id=customer_id))
  else:
    # Log error messages to user
    if form.errors:
      for error in form.errors.values():
        flash(error[0], "danger")
    return render_template("make-contact.html", title="New Contact", customer_id=customer_id, form=form)

# Contact - Edit Contact
@contact_routes.route("/edit-contact/<int:contact_id>", methods=["GET", "POST"])
@login_required
def edit_contact(contact_id):
  contact = Contact.query.get(contact_id)
  # Create form
  edit_form = CreateContactForm(
    name=contact.name,
    role=contact.role,
    email=contact.email,
    phone=contact.phone,
  )
  # Update contact information
  if edit_form.validate_on_submit():
    contact.name = edit_form.name.data
    contact.role = edit_form.role.data
    contact.email = edit_form.email.data.lower()
    contact.phone = edit_form.phone.data
    db.session.commit()
    # Log message to user
    flash("Contact has been updated.", "success")
    return redirect(url_for("customer.show_customer", customer_id=contact.customer_id))
  else:
    # Log error messages to user
    if edit_form.errors:
      for error in edit_form.errors.values():
        flash(error[0], "danger")
    return render_template("make-contact.html", title="Edit Contact", form=edit_form, is_edit=True, contact_id=contact.id)

# Contact - Delete Contact
@contact_routes.route("/delete-contact/<int:contact_id>", methods=["GET"])
@login_required
@admin_only
def delete_contact(contact_id):
  # Get user to delete
  contact_to_delete = Contact.query.get(contact_id)
  to_return = contact_to_delete.customer_id
  # Delete contact
  db.session.delete(contact_to_delete)
  db.session.commit()
  # Log message to user
  flash("Contact has been deleted.", "danger")
  return redirect(url_for('customer.show_customer', customer_id=to_return))
