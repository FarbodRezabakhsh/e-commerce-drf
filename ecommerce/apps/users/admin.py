from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
# Register your models here.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    ordering = ['id']
    list_display = ['email', 'is_staff', 'is_active']
    search_fields = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ("Permissions", {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ("Important dates", {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )