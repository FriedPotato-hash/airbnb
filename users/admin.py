from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models her


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    # list_display = ("username","gender", "language", "currency", "superhost")
    # list_filter = ("superhost", "language", "currency")
    fieldsets = UserAdmin.fieldsets + (
        ("Banana", {"fields": ("avatar", "gender", "currency")}),
    )
    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_superuser",
    )
