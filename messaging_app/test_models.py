# tests/test_models.py
import pytest
from django.test import TestCase
from listings.models import Booking, Payment

class TestPaymentModel(TestCase):
    def test_payment_creation(self):
        """Test payment model creation."""
        payment = Payment.objects.create(
            amount=100.00,
            status='pending'
        )
        self.assertEqual(str(payment), f"{payment.tx_ref} - pending")
        
    def test_payment_status_choices(self):
        """Test payment status choices."""
        payment = Payment()
        self.assertIn(('pending', 'Pending'), payment.STATUS_CHOICES)
        
@pytest.mark.django_db
def test_booking_creation():
    """Test booking creation using pytest."""
    booking = Booking.objects.create(
        user_id=1,
        check_in='2024-12-25',
        check_out='2024-12-31'
    )
    assert booking is not None
