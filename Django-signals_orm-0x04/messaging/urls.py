from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('delete-account/', views.delete_user_account, name='delete_account'),
    
    # Threaded conversation URLs
    path('threads/', views.thread_list, name='thread_list'),
    path('threads/create/', views.create_thread_starter, name='create_thread'),
    path('threads/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('reply/<int:parent_message_id>/', views.create_reply, name='create_reply'),
    path('thread/<int:message_id>/replies/', views.get_thread_replies, name='get_replies'),
    path('thread/<int:message_id>/recursive/', views.get_recursive_thread, name='get_recursive_thread'),
    
    # NEW: Unread messages URLs
    path('unread/', views.unread_messages_inbox, name='unread_inbox'),
    path('unread/api/', views.unread_messages_api, name='unread_api'),
    path('unread/threads/', views.unread_threads_api, name='unread_threads_api'),
    path('mark-read/', views.mark_messages_read, name='mark_messages_read'),
    path('mark-read/<int:message_id>/', views.mark_single_message_read, name='mark_single_read'),
]