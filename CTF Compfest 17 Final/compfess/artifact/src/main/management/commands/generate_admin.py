import os
import string
import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Profile  

CHARSET = (string.ascii_letters + string.digits + string.punctuation).replace(" ", "")

def generate_password(length: int = 16) -> str:
    return "".join(secrets.choice(CHARSET) for _ in range(length))

class Command(BaseCommand):

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )

        if created:
            password = open("/secret/password.txt", "r").read().strip()
            # password = generate_password(16)
            user.set_password(password)
            user.save()
            Profile.objects.get_or_create(user=user,role = 'admin')
            self.stdout.write(self.style.SUCCESS(
                f"[ensure_admin] Created admin '{username}' with password: {password}"
            ))
        else:
            changed = False
            if not user.is_staff:
                user.is_staff = True; changed = True
            if not user.is_superuser:
                user.is_superuser = True; changed = True
            if changed:
                user.save()
            Profile.objects.get_or_create(user=user,role = 'admin')
            self.stdout.write(self.style.WARNING(
                f"[ensure_admin] Admin '{username}' already exists (password unchanged)."
            ))
