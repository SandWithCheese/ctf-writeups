from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import (HttpResponseForbidden, HttpResponseBadRequest,
                         FileResponse)
from django.views.decorators.http import require_http_methods
from django.conf import settings
from uuid import UUID, uuid4
from .auth import is_admin
from .filter import *
from .models import Profile, Menfess
from .forms import RegisterForm, ProfileForm, MenfessForm
from django.template import engines
from urllib.parse import urlparse
from .reports import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


from pathlib import Path

import tarfile
import zipfile

TMP_DIR = Path("/tmp")


def index(request):
    menfesses = Menfess.objects.select_related('recipient', 'sender_user')[:50]
    return render(request, 'index.html', {
        'menfesses': menfesses,
        'cur_user': request.user if request.user.is_authenticated else None,
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            Profile.objects.create(user=user)
            return redirect('main:login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile_view(request, id: UUID):
    profile = get_object_or_404(Profile.objects.select_related('user'), pk=id)
    profile_user = profile.user

    jinja = engines['jinja2']

    if not (is_admin(request.user) or request.user.id == profile_user.id):
        return HttpResponseForbidden("You can only view your own profile.")

    try:
        rendered_bio = jinja.from_string(profile.bio or '').render()
    except Exception:
        rendered_bio = "<em>Invalid bio template.</em>"

    inbox = profile_user.received_menfess.select_related('sender_user')[:50]
    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'rendered_bio': rendered_bio,
        'inbox': inbox,
        'cur_user': request.user,
    })


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main:profile', id=profile.id)  
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form, 'cur_user': request.user})


def send_menfess(request):
    if request.method == 'POST':
        form = MenfessForm(request.POST)
        if form.is_valid():
            mf = form.save(commit=False)
            if request.user.is_authenticated:
                mf.sender_user = request.user
                mf.is_guest = False
            else:
                mf.is_guest = True
            mf.save()
            return redirect('main:index')
    else:
        form = MenfessForm()
    return render(request, 'send_menfess.html', {
        'form': form,
        'cur_user': request.user if request.user.is_authenticated else None
    })


def feed(request):
    menfesses = Menfess.objects.select_related('recipient', 'sender_user')[:100]
    return render(request, 'feed.html', {
        'menfesses': menfesses,
        'cur_user': request.user if request.user.is_authenticated else None,
    })

def feed_by_sender(request):
    sender = (request.GET.get('sender') or '').strip()
    menfesses = []
    
    if not sender:
        rows = []
    elif sender.lower() == 'guest':
        menfesses = filter_by_guest()


    else:
        if sender.lower() == 'me' and request.user.is_authenticated:
            username = request.user.username
            menfesses = filter_by_sender(username)
        else:
            username = sender
            menfesses = filter_by_sender(username)

    return render(request, 'feed.html', {
        'menfesses': menfesses,
        'cur_user': request.user if request.user.is_authenticated else None,
    })

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'GET':
        class LoginForm(RegisterForm):
            class Meta:
                pass
        form = LoginForm()
        form.fields.pop('email', None)
        form.fields['password'].widget.input_type = 'password'
        return render(request, 'login.html', {
            'form': form,
            'cur_user': request.user if request.user.is_authenticated else None
        })

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    serializer = TokenObtainPairSerializer(data={'username': username, 'password': password})
    if not serializer.is_valid():
        return render(request, 'login.html', {'form': None, 'error': 'Invalid credentials'})

    tokens = serializer.validated_data
    resp = redirect('main:index')

    access_cookie = settings.SIMPLE_JWT.get('AUTH_COOKIE', 'jwt_access')
    refresh_cookie = settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'jwt_refresh')
    samesite = settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax')
    secure = settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False)
    httponly = settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY', True)

    access_seconds = int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
    refresh_seconds = int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())

    resp.set_cookie(access_cookie, tokens['access'], max_age=access_seconds, httponly=httponly, secure=secure, samesite=samesite, path='/')
    resp.set_cookie(refresh_cookie, tokens['refresh'], max_age=refresh_seconds, httponly=httponly, secure=secure, samesite=samesite, path='/')
    return resp


def logout_view(request):
    resp = redirect('main:index')
    access_cookie = settings.SIMPLE_JWT.get('AUTH_COOKIE', 'jwt_access')
    refresh_cookie = settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'jwt_refresh')
    resp.delete_cookie(access_cookie, path='/')
    resp.delete_cookie(refresh_cookie, path='/')
    return resp


@require_http_methods(["POST"])
def refresh_view(request):
    refresh_cookie = settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'jwt_refresh')
    raw_refresh = request.COOKIES.get(refresh_cookie)
    if not raw_refresh:
        return redirect('main:login')

    try:
        token = RefreshToken(raw_refresh)
        new_access = str(token.access_token)
    except Exception:
        return redirect('main:login')

    resp = redirect('main:index')
    access_cookie = settings.SIMPLE_JWT.get('AUTH_COOKIE', 'jwt_access')
    samesite = settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax')
    secure = settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False)
    httponly = settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY', True)
    access_seconds = int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
    resp.set_cookie(access_cookie, new_access, max_age=access_seconds, httponly=httponly, secure=secure, samesite=samesite, path='/')
    return resp

def _require_admin(request):
    if not (request.user.is_authenticated and is_admin(request.user)):
        return HttpResponseForbidden("Admin only.")
    return None

def _write_report_file(username: str, content: str) -> Path:
    rid = str(uuid4())
    filename = f"{rid}.txt"
    path = settings.REPORT_DIR / filename
    body = f"Creator: {username}\n\n{content}\n"
    path.write_text(body, encoding="utf-8")
    return path


@login_required
def reports(request):
    if (resp := _require_admin(request)) is not None:
        return resp
    return render(request, "reports.html", {"cur_user": request.user})


@login_required
def create_report(request):

    if (resp := _require_admin(request)) is not None:
        return resp
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    
    reports_dir = settings.REPORT_DIR
    
    up = request.FILES.get("file")

    if up:
        name = getattr(up, "name", "upload")
        lower = name.lower()

        try:
            if lower.endswith(".txt"):
                dest = (reports_dir / name).resolve()
                root = reports_dir.resolve()
                if root not in dest.parents and dest != root:
                    return HttpResponseBadRequest("Invalid destination path")
                with open(dest, "wb") as fh:
                    for chunk in up.chunks():
                        fh.write(chunk)
                messages.success(request, f"Saved text to {dest.name}")
                return redirect("main:admin_reports")

            elif lower.endswith(".zip"):
                arc_path = (TMP_DIR / name).with_suffix(".zip")
                with open(arc_path, "wb") as fh:
                    for chunk in up.chunks():
                        fh.write(chunk)
                try:
                    with zipfile.ZipFile(arc_path, "r") as zf:
                        ok, msg = extract_zip(zf, reports_dir)
                finally:
                    try: arc_path.unlink(missing_ok=True)
                    except Exception: pass
                if not ok:
                    return HttpResponseBadRequest(msg)
                messages.success(request, "ZIP extracted into /tmp/reports")
                return redirect("main:admin_reports")

            elif lower.endswith(".tar"):
                arc_path = (TMP_DIR / name).with_suffix(".tar")
                with open(arc_path, "wb") as fh:
                    for chunk in up.chunks():
                        fh.write(chunk)
                try:
                    with tarfile.open(arc_path, "r") as tfobj:
                        ok, msg = extract_tar(tfobj, reports_dir)
                finally:
                    try: arc_path.unlink(missing_ok=True)
                    except Exception: pass
                if not ok:
                    return HttpResponseBadRequest(msg)
                messages.success(request, "TAR extracted into /tmp/reports")
                return redirect("main:admin_reports")

            else:
                return HttpResponseBadRequest("Only .txt, .zip, or .tar files are accepted")

        except (zipfile.BadZipFile, tarfile.ReadError) as e:
            return HttpResponseBadRequest(f"Invalid archive: {e}")
        except Exception as e:
            return HttpResponseBadRequest(f"Upload failed: {e}")

    content = (request.POST.get("content") or "").strip()
    if not content:
        content = f"Report created by {request.user.username}"

    path = _write_report_file(request.user.username, content)
    rid = path.stem  
    return redirect("main:admin_report_detail", rid=rid)

@login_required
def report_detail(request, rid: UUID):

    if (resp := _require_admin(request)) is not None:
        return resp

    name = f"{str(rid)}.txt"
    fs_path = (settings.REPORT_DIR / name).resolve()

    exists = fs_path.exists()

    file_url = f"file://{fs_path.as_posix()}"

    return render(
        request,
        "report_detail.html",
        {"cur_user": request.user, "rid": str(rid), "exists": exists, "file_url": file_url},
    )

@login_required
def download_report(request):
    if (resp := _require_admin(request)) is not None:
        return resp
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    raw_url = (request.POST.get("url") or "").strip()
    if not raw_url:
        return HttpResponseBadRequest("Missing 'url'")
    
    return validate_url(raw_url)






