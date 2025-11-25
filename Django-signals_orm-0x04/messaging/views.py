from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@login_required
@require_http_methods(["GET", "POST"])
def delete_user_account(request):
    """
    View to allow users to delete their own account
    """
    if request.method == 'POST':
        try:
            # Get confirmation from request
            data = json.loads(request.body) if request.body else {}
            confirm_delete = data.get('confirm_delete', False)
            
            if confirm_delete:
                user = request.user
                username = user.username
                
                # Logout the user first
                logout(request)
                
                # Delete the user (this will trigger our post_delete signal)
                user.delete()
                
                # Return success response
                return JsonResponse({
                    'success': True,
                    'message': f'Account {username} has been successfully deleted. All your data has been removed.'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Please confirm account deletion.'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error deleting account: {str(e)}'
            }, status=500)
    
    # GET request - show confirmation page
    return render(request, 'messaging/delete_account_confirm.html')

@login_required
def user_profile(request):
    """
    User profile page with deletion option
    """
    user = request.user
    stats = {
        'sent_messages': user.sent_messages.count(),
        'received_messages': user.received_messages.count(),
        'notifications': user.notifications.count(),
    }
    
    return render(request, 'messaging/user_profile.html', {
        'user': user,
        'stats': stats
    })
