from django.urls import path
from . import views

urlpatterns = [
    path('delete-account/', views.account_delete, name='account_delete'),
    path('conversation/<int:user_id>/', views.conversation_view, name='conversation'),
    path('unread/', views.unread_view, name='unread'),
    path('message/<int:message_id>/history/', views.message_history_view, name='history'),
]