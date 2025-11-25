from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q, Count, Case, When, Value, IntegerField
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch, Q, Count
from .models import Message, ConversationThread

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


@login_required
def thread_list(request):
    """
    View to display all conversation threads for the user
    Uses prefetch_related and select_related for optimization
    """
    user = request.user
    
    # Get threads with optimized queries
    threads = Message.objects.get_threads_for_user(user)
    
    # Annotate with reply counts
    threads = threads.annotate(
        total_replies=Count('replies')
    )
    
    return render(request, 'messaging/thread_list.html', {
        'threads': threads,
        'user': user
    })

@login_required
def thread_detail(request, thread_id):
    """
    View to display a complete thread with all replies
    Uses advanced ORM techniques for efficient querying
    """
    user = request.user
    
    # Get the complete thread with all replies using optimized queries
    thread_messages = Message.objects.get_complete_thread(thread_id)
    
    # Verify user has access to this thread
    thread_starter = get_object_or_404(Message, id=thread_id)
    if user not in [thread_starter.sender, thread_starter.receiver]:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Organize messages by depth for template rendering
    organized_messages = {}
    for message in thread_messages:
        if message.thread_depth not in organized_messages:
            organized_messages[message.thread_depth] = []
        organized_messages[message.thread_depth].append(message)
    
    return render(request, 'messaging/thread_detail.html', {
        'thread_starter': thread_starter,
        'organized_messages': organized_messages,
        'max_depth': max(organized_messages.keys()) if organized_messages else 0,
        'user': user
    })

@login_required
@require_http_methods(["POST"])
def create_reply(request, parent_message_id):
    """
    View to create a reply to a message
    """
    user = request.user
    
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Content is required'}, status=400)
        
        # Get parent message
        parent_message = get_object_or_404(Message, id=parent_message_id)
        
        # Verify user can reply to this message
        if user not in [parent_message.sender, parent_message.receiver]:
            return JsonResponse({'error': 'Cannot reply to this message'}, status=403)
        
        # Create reply
        reply = Message.objects.create(
            sender=user,
            receiver=parent_message.sender,  # Reply goes to original sender
            content=content,
            parent_message=parent_message
        )
        
        # Return the reply data with optimized related fields
        reply_data = {
            'id': reply.id,
            'content': reply.content,
            'timestamp': reply.timestamp.isoformat(),
            'sender': {
                'id': reply.sender.id,
                'username': reply.sender.username
            },
            'thread_depth': reply.thread_depth,
            'parent_message_id': reply.parent_message_id
        }
        
        return JsonResponse({
            'success': True,
            'message': 'Reply sent successfully',
            'reply': reply_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_thread_replies(request, message_id):
    """
    API endpoint to get replies for a specific message
    Uses recursive-like query with optimization
    """
    user = request.user
    
    try:
        message = get_object_or_404(Message, id=message_id)
        
        # Verify access
        if user not in [message.sender, message.receiver]:
            return JsonResponse({'error': 'Access denied'}, status=403)
        
        # Get replies with optimized queries
        replies = message.get_thread_replies(include_self=False)
        
        # Convert to nested structure for frontend
        def build_reply_tree(messages, parent_id=None):
            tree = []
            for msg in messages:
                if msg.parent_message_id == parent_id:
                    node = {
                        'id': msg.id,
                        'content': msg.content,
                        'timestamp': msg.timestamp.isoformat(),
                        'sender': {
                            'id': msg.sender.id,
                            'username': msg.sender.username
                        },
                        'thread_depth': msg.thread_depth,
                        'replies': build_reply_tree(messages, msg.id)
                    }
                    tree.append(node)
            return tree
        
        # Filter to only include replies to the specified message
        reply_messages = [msg for msg in replies if msg.parent_message_id == message_id]
        reply_tree = build_reply_tree(reply_messages, message_id)
        
        return JsonResponse({
            'success': True,
            'replies': reply_tree,
            'count': len(reply_messages)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def create_thread_starter(request):
    """
    View to create a new thread starter message
    """
    user = request.user
    
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        receiver_id = data.get('receiver_id')
        
        if not content or not receiver_id:
            return JsonResponse({'error': 'Content and receiver are required'}, status=400)
        
        receiver = get_object_or_404(User, id=receiver_id)
        
        # Create thread starter (no parent message)
        message = Message.objects.create(
            sender=user,
            receiver=receiver,
            content=content
            # parent_message is None by default for thread starters
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Thread started successfully',
            'thread_id': message.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)