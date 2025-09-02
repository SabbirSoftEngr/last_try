from django.contrib import admin
from .models import Profile, BloodRequest, Donation

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'blood_group', 'available', 'last_donation_date')
    list_filter = ('blood_group', 'available')

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'blood_group', 'status', 'needed_date', 'created_at')
    list_filter = ('blood_group', 'status')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'request', 'status', 'created_at')
    list_filter = ('status',)
