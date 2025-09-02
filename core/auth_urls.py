from django.urls import path
from .views import register_view, login_view, logout_view, verify_email, verification_sent, resend_verification


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify/sent/', verification_sent, name='verification_sent'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('verify/resend/', resend_verification, name='resend_verification'),
]
