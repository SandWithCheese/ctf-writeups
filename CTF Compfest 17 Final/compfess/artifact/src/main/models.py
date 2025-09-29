from django.db import models
from django.contrib.auth.models import User
import uuid
class Profile(models.Model):
    ROLE_CHOICES = [
        ('participant', 'Participant'),
        ('probset', 'Probset'),
        ('admin', 'Admin'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=128, default='')
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='participant')

    def __str__(self):
        return f"Profile({self.user.username})"


class Menfess(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    sender_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_menfess')
    is_guest = models.BooleanField(default=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_menfess')

    def sender_label(self):
        if self.is_guest or not self.sender_user:
            return 'Guest'
        return self.sender_user.username

    class Meta:
        ordering = ['-created_at']
