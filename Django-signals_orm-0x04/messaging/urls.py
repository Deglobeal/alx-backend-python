from django.urls import path
from . import views

urlpatterns = [
    path('delete-user/', views.delete_user, name='delete_user'),
    path('conversation/<int:user_id>/', views.conversation_thread, name='conversation_thread'),
    path('reply/<int:parent_id>/', views.create_reply, name='create_reply'),
    path('unread/', views.unread_messages, name='unread_messages'),
    path('message/<int:message_id>/history/', views.message_history, name='message_history'),
]