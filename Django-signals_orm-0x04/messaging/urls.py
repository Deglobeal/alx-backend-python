from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.user_notifications, name='user_notifications'),
    path('', views.message_list, name='message_list'),
    path('message/<int:message_id>/history/', views.message_history, name='message_history'),
]