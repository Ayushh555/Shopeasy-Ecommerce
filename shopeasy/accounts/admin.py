from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'pincode')
    search_fields = ('user__username', 'user__email', 'phone', 'city')
