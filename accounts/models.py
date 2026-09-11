from django.db import models
from django.contrib.auth.models import User

# Comment 1: UserProfile extends the built-in Django User model with custom demographic fields.
# Comment 2: Establishes a 1-to-1 relationship with auth_user for user management and profile details.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Comment 3: Display string representation showing full name or fallback to username.
    def __str__(self):
        return f"{self.full_name or self.user.username}'s Profile"
