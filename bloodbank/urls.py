from django.contrib import admin
from django.urls import path, include
from core.views import home
from core.views import AboutView, PrivacyView, TermsView, ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('core.auth_urls')),
    path('', home, name='home'),
    path('dashboard/', include('core.dashboard_urls')),

    path('about/', AboutView.as_view(), name='about'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('contact/', ContactView.as_view(), name='contact'),
]
