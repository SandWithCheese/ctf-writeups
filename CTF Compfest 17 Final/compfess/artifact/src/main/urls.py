from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/refresh/', views.refresh_view, name='refresh'),

    path('u/<uuid:id>/', views.profile_view, name='profile'),
    path('u/me/edit/', views.edit_profile, name='edit_profile'),

    path('send/', views.send_menfess, name='send'),
    path('feed/', views.feed, name='feed'),

    path('feed/by-sender/', views.feed_by_sender, name='feed_by_sender'),

    path("admin/reports/", views.reports, name="admin_reports"),
    path("admin/reports/new", views.create_report, name="admin_report_create"),
    path("admin/reports/<uuid:rid>/", views.report_detail, name="admin_report_detail"),
    path("admin/reports/download", views.download_report, name="admin_report_download_by_url"),
]
