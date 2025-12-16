import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from alx_travel_app.listings.models import Payment, Booking
from datetime import datetime, timedelta

class TestPaymentModel(TestCase):
    def test_payment_creation(self):
        """Test creating a payment record."""
        user = User.objects.create_user('testuser', 'test@example.com', 'password123')
        booking = Booking.objects.create(
            user=user,
            check_in=datetime.now(),
            check_out=datetime.now() + timedelta(days=3),
            amount=150.00
        )
        
        payment = Payment.objects.create(
            booking=booking,
            amount=150.00,
            status='pending',
            tx_ref='test-ref-123'
        )
        
        self.assertEqual(payment.status, 'pending')
        self.assertEqual(str(payment), f"{payment.tx_ref} - pending")
        
    @pytest.mark.django_db
    def test_payment_status_choices(self):
        """Test payment status choices are valid."""
        payment = Payment()
        choices = dict(payment.STATUS_CHOICES)
        self.assertIn('pending', choices)
        self.assertIn('successful', choices)
        self.assertIn('failed', choices)
        