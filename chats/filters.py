import django_filters
from .models import Message
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class MessageFilter(django_filters.FilterSet):
    """
    Filter class for messages with various filtering options
    """
    # Filter by conversation with specific user (username)
    participant = django_filters.CharFilter(
        method='filter_by_participant',
        label='Filter by participant username'
    )
    
    # Filter by time range
    start_date = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='gte',
        label='Messages from this date/time'
    )
    
    end_date = django_filters.DateTimeFilter(
        field_name='timestamp', 
        lookup_expr='lte',
        label='Messages until this date/time'
    )
    
    # Filter by conversation ID
    conversation = django_filters.NumberFilter(
        field_name='conversation__id',
        label='Filter by conversation ID'
    )
    
    # Filter by read status
    read = django_filters.BooleanFilter(
        field_name='read',
        label='Filter by read status'
    )
    
    # Filter by sender
    sender = django_filters.CharFilter(
        field_name='sender__username',
        lookup_expr='icontains',
        label='Filter by sender username'
    )
    
    # Recent messages (last N hours)
    recent_hours = django_filters.NumberFilter(
        method='filter_recent_messages',
        label='Messages from last N hours'
    )
    
    class Meta:
        model = Message
        fields = [
            'conversation', 
            'sender', 
            'read', 
            'start_date', 
            'end_date',
            'participant',
            'recent_hours'
        ]
    
    def filter_by_participant(self, queryset, name, value):
        """
        Filter messages by conversations with a specific participant (username)
        """
        try:
            user = User.objects.get(username=value)
            return queryset.filter(conversation__participants=user)
        except User.DoesNotExist:
            return queryset.none()
    
    def filter_recent_messages(self, queryset, name, value):
        """
        Filter messages from the last N hours
        """
        if value:
            time_threshold = timezone.now() - timedelta(hours=value)
            return queryset.filter(timestamp__gte=time_threshold)
        return queryset