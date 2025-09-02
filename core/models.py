from django.db import models
from django.contrib.auth.models import User

BLOOD_GROUPS = [
    ('O+', 'O+'), ('O-', 'O-'),
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, default='O+')
    last_donation_date = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=False)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.blood_group})"

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('ACCEPTED', 'Accepted'),
        ('CANCELED', 'Canceled'),
        ('COMPLETED', 'Completed'),
    ]
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units = models.PositiveIntegerField(default=1)
    hospital = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    needed_date = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request #{self.id} for {self.blood_group} by {self.requester.username}"

class Donation(models.Model):
    STATUS_CHOICES = [
        ('PLEDGED', 'Pledged'),
        ('CANCELED', 'Canceled'),
        ('DONATED', 'Donated'),
    ]
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    request = models.OneToOneField(BloodRequest, on_delete=models.CASCADE, related_name='donation')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PLEDGED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation {self.id} -> Request {self.request_id} ({self.status})"
