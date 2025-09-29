from django.contrib import admin
from .models import Profile, Menfess

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)

@admin.register(Menfess)
class MenfessAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'sender_user', 'is_guest', 'created_at')
    list_filter = ('is_guest',)
    search_fields = ('content', 'recipient__username', 'sender_user__username')
