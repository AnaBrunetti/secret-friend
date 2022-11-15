from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from accounts.models import (
    User,
    Profissional,
)

User = get_user_model()


class UserProfissionalInline(admin.StackedInline):
    model = Profissional
    fields = ["phone", "picture", "document", "cpf", "is_approved"]
    extra = 0


@ admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "username", "email", "first_name", "role", "gender", "is_staff",  "is_superuser", "is_active"
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "role", "gender"]
    filter_horizontal = ["groups", "user_permissions"]
    readonly_fields = ["last_login", "date_joined", "updated_at"]
    fieldsets = [
        [None, {
            "fields": ["username", "password"]
        }],
        ["Personal info", {
            "fields": ["email", "first_name", "last_name", "role", "gender", "date_of_birth"]
        }],
        ["Permissions", {
            "fields": ["is_active", "is_staff", "is_superuser", "groups", "user_permissions"]
        }],
        ["Important dates", {
            "classes": ["collapse"],
            "fields": ["last_login", "date_joined", "updated_at"]
        }]
    ]
    add_fieldsets = [
        [None, {
            "classes": ["wide"],
            "fields": ["username", "password1", "password2"]
        }]
    ]
    search_fields = ["username", "email", "first_name", "last_name"]
    list_per_page = 12
    ordering = ["username"]
    inlines = [UserProfissionalInline]
