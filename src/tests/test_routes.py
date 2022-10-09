from ..main import app

# Unauthenticated request to /login route
def test_unauthenticated_login_route():
    client = app.test_client()
    response = client.get("/login")
    assert response.status_code == 200

# Unauthenticated request to /home route
def test_unauthenticated_home_request():
    client = app.test_client()
    response = client.get("/home")
    assert response.status_code == 404

# Unauthenticated request to /create-user route
def test_unauthenticated_create_user_request():
    client = app.test_client()
    response = client.get("/create-user")
    assert response.status_code == 302

# Unauthenticated request to /change-password route
def test_unauthenticated_change_password_request():
    client = app.test_client()
    response = client.get("/change-password")
    assert response.status_code == 302

# Unauthenticated request to /admin-panel route
def test_unauthenticated_admin_panel_request():
    client = app.test_client()
    response = client.get("/admin-panel")
    assert response.status_code == 302

# Unauthenticated request to /customer route
def test_unauthenticated_customer_request():
    client = app.test_client()
    response = client.get("/customer")
    assert response.status_code == 302

# Unauthenticated request to /new-customer route
def test_unauthenticated_new_customer_request():
    client = app.test_client()
    response = client.get("/new-customer")
    assert response.status_code == 302

# Unauthenticated request to /sale route
def test_unauthenticated_sales_request():
    client = app.test_client()
    response = client.get("/sale")
    assert response.status_code == 302
