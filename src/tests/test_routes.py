from ..main import app

def test_login_route():
    client = app.test_client()
    response = client.get("/login")
    assert response.status_code == 200
  
def test_unauthorised_home_request():
    client = app.test_client()
    response = client.get("/home")
    assert response.status_code == 404

def test_unauthorised_create_user_request():
    client = app.test_client()
    response = client.get("/create-user")
    assert response.status_code == 302

def test_unauthorised_change_password_request():
    client = app.test_client()
    response = client.get("/change-password")
    assert response.status_code == 302

def test_unauthorised_admin_panel_request():
    client = app.test_client()
    response = client.get("/admin-panel")
    assert response.status_code == 302

def test_unauthorised_customer_request():
    client = app.test_client()
    response = client.get("/customer")
    assert response.status_code == 302

def test_unauthorised_new_customer_request():
    client = app.test_client()
    response = client.get("/new-customer")
    assert response.status_code == 302

def test_unauthorised_sales_request():
    client = app.test_client()
    response = client.get("/sale")
    assert response.status_code == 302




    