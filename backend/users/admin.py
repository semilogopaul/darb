from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_approved')
    list_filter = ('user_type', 'is_approved')
    search_fields = ('username', 'email')
