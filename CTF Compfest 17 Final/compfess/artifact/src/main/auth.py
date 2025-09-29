from django.conf import settings

def is_admin(user) -> bool:
    """
    Admin = authenticated AND (username, email) pair is in settings.ADMIN_ACCOUNTS.
    """
    try:
        if not (user and user.is_authenticated):
            return False
        uname = getattr(settings, "ADMIN_USERNAME", None)
        email = getattr(settings, "ADMIN_EMAIL", None)
        u = getattr(user, "username", "")
        e = (getattr(user, "email", "") or "")
        if u == uname and e == email:
            return True
        return False
    except Exception:
        return False
