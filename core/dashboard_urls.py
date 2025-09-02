from django.urls import path
from .views import (
    dashboard_index, edit_profile, create_request, list_recipient_requests,
    accept_request, cancel_request, mark_donated, donation_history
)

urlpatterns = [
    path('', dashboard_index, name='dashboard'),
    path('profile/', edit_profile, name='edit_profile'),
    path('request/new/', create_request, name='create_request'),
    path('requests/', list_recipient_requests, name='recipient_requests'),
    path('requests/<int:pk>/accept/', accept_request, name='accept_request'),
    path('requests/<int:pk>/cancel/', cancel_request, name='cancel_request'),
    path('requests/<int:pk>/donated/', mark_donated, name='mark_donated'),
    path('history/', donation_history, name='donation_history'),
]
