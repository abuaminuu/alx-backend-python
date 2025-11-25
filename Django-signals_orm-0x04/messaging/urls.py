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
    
    # UPDATED: Unread messages URLs with simpler patterns
    path('unread/', views.unread_messages_inbox, name='unread_inbox'),
    path('unread/api/', views.unread_messages_api, name='unread_api'),
    path('unread/threads/', views.unread_threads_api, name='unread_threads_api'),
    path('mark-read/', views.mark_messages_read, name='mark_messages_read'),
    path('mark-read/<int:message_id>/', views.mark_single_message_read, name='mark_single_read'),
    path('unread/simple/', views.simple_unread_view, name='simple_unread'),
    path('mark-read/', views.mark_messages_read, name='mark_messages_read'),
    
    # NEW: Main inbox
    path('inbox/', views.user_inbox, name='user_inbox'),
    path('unread/threads/', views.unread_threads_view, name='unread_threads'),
    path('profile/', views.user_profile, name='user_profile'),
    path('delete-account/', views.delete_user_account, name='delete_account'),
    
    # Cached views (60 seconds cache)
    path('threads/', views.thread_list, name='thread_list'),  # Cached
    path('threads/cached-class/', views.CachedThreadListView.as_view(), name='cached_thread_list_class'),  # Cached class-based
    path('threads/<int:thread_id>/', views.thread_detail, name='thread_detail'),  # Cached
    path('threads/<int:thread_id>/cached-advanced/', views.cached_thread_detail_advanced, name='cached_thread_detail_advanced'),  # Manual cache
    path('unread/', views.unread_messages_inbox, name='unread_inbox'),  # Cached
    path('inbox/', views.user_inbox, name='user_inbox'),  # Cached
    
    # Non-cached views (dynamic content)
    path('unread/api/', views.unread_messages_api, name='unread_api'),  # Not cached
    path('reply/<int:parent_message_id>/', views.create_reply, name='create_reply'),  # Not cached
    path('mark-read/', views.mark_messages_read, name='mark_messages_read'),  # Not cached
    path('threads/create/', views.create_thread_starter, name='create_thread'),  # Not cached
    path('thread/<int:message_id>/replies/', views.get_thread_replies, name='get_replies'),  # Not cached
    path('thread/<int:message_id>/recursive/', views.get_recursive_thread, name='get_recursive_thread'),  # Not cached
    # Cache management URLs
    path('cache/clear/', views.clear_cache_view, name='clear_cache'),
    path('cache/info/', views.cache_info_view, name='cache_info'),
]