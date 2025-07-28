import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username')
    start_date = django_filters.DateTimeFilter(
        field_name='sent_at', 
        lookup_expr='gte',
        label='Messages after this date/time'
    )
    end_date = django_filters.DateTimeFilter(
        field_name='sent_at', 
        lookup_expr='lte',
        label='Messages before this date/time'
    )
    
    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']