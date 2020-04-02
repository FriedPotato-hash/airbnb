from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ResearvationAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)
