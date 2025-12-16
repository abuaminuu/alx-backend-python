import json
import pytest
from django.urls import reverse
from django.test import Client
from model_bakery import baker
from alx_travel_app.listings.models import Booking

@pytest.mark.django_db
class TestBookingViews:
    def test_create_booking(self, authenticated_client):
        """Test creating a booking via API."""
        client, user = authenticated_client
        
        data = {
            'check_in': '2024-12-25',
            'check_out': '2024-12-31',
            'guests': 2,
            'special_requests': 'Test request'
        }
        
        response = client.post(
            reverse('booking-create'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert 'id' in response.json()
        
    def test_payment_initiation(self, client, mocker):
        """Test payment initiation endpoint."""
        # Mock Chapa API
        mock_chapa = mocker.patch('alx_travel_app.listings.services.ChapaPaymentService.initialize_payment')
        mock_chapa.return_value = {
            'status': 'success',
            'data': {
                'checkout_url': 'https://checkout.chapa.co/test',
                'tx_ref': 'test-ref-123'
            }
        }
        
        booking = baker.make(Booking)
        
        response = client.post(
            reverse('initialize-payment', kwargs={'booking_id': booking.id}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'checkout_url' in response.json()
    