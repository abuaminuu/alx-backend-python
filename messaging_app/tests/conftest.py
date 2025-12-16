import pytest
from django.test import Client
from django.contrib.auth.models import User
from model_bakery import baker

@pytest.fixture
def client():
    """Provides a Django test client."""
    return Client()

@pytest.fixture
def authenticated_client():
    """Provides a Django test client with authenticated user."""
    client = Client()
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword123'
    )
    client.force_login(user)
    return client, user

@pytest.fixture
def test_user(db):
    """Creates a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword123'
    )

@pytest.fixture
def admin_user(db):
    """Creates an admin user."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword123'
    )

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enables database access for all tests."""
    pass

@pytest.fixture
def mock_chapa_response(mocker):
    """Mocks Chapa API responses."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {
            "checkout_url": "https://checkout.chapa.co/checkout/123",
            "tx_ref": "tx-ref-12345",
            "status": "pending"
        }
    }
    return mock_response
    