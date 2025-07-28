# messaging_app/chats/filters.py

import django_filters
from .models import Message
from django.contrib.auth.models import User
from django.utils import timezone

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    recipient = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    created_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'created_after', 'created_before']
