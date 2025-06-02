from django.db import models
from django.contrib.auth.models import User
import random
import string
from datetime import timedelta
from django.utils import timezone


ACTIVITY_CHOICES = [
    ("Case Supervision", "Case Supervision"),
    ("Client Consultation", "Client Consultation"),
    ("Legal Research", "Legal Research"),
    ("Drafting of Pleadings or affidavits", "Drafting of Pleadings or affidavits"),
    ("Court Appearances", "Court Appearances"),
    ("Mediation or ADR Facilitation", "Mediation or ADR Facilitation"),
    ("Training or Lectures for Law Interns", "Training or Lectures for Law Interns"),
    ("Community Legal Education", "Community Legal Education"),
    ("Other", "Other (Please specify)"),
]


class ULASActivity(models.Model):
    activity_type = models.CharField(max_length=255, choices=ACTIVITY_CHOICES)
    description = models.TextField()
    students_supervised = models.PositiveIntegerField(null=True, blank=True)
    clients_served = models.PositiveIntegerField(null=True, blank=True)
    date_of_activity = models.DateField()
    hours_rendered = models.DecimalField(max_digits=5, decimal_places=2)
    proof_image = models.ImageField(upload_to='proofs/', null=True, blank=True)

    def __str__(self):
        return self.activity_type


class ActivityLog(models.Model):
    action = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} performed {self.action} on {self.timestamp}'


class Activity(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255, choices=ACTIVITY_CHOICES)
    description = models.TextField()
    number_of_students = models.PositiveIntegerField(default=0)
    number_of_clients = models.PositiveIntegerField(default=0)
    date = models.DateField()
    hours_rendered = models.DecimalField(max_digits=5, decimal_places=2)
    proof = models.ImageField(upload_to='proofs/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # ✅ NEW FIELD

    def __str__(self):
        return f"{self.activity_type} on {self.date}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    year_admitted = models.CharField(max_length=10)
    office_name = models.CharField(max_length=100, blank=True)
    law_school = models.CharField(max_length=100)
    work_cell = models.CharField(max_length=20, blank=True)
    roll_number = models.CharField(max_length=20)
    sector = models.CharField(max_length=50)
    office_address = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    is_approved = models.BooleanField(null=True, default=None)

    def __str__(self):
        return self.user.username

class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    @classmethod
    def generate_code(cls):
        return ''.join(random.choices(string.digits, k=6))

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def verify(self, code):
        if not self.is_expired() and code == self.code:
            self.is_verified = True
            self.save()
            return True
        return False

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=15)

    @classmethod
    def generate_code(cls):
        return ''.join(random.choices(string.digits, k=6))
