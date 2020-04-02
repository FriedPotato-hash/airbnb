from django.contrib import admin
from . import models


@admin.register(models.List)
class Listadmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "count_rooms",
    )
    serach_fileds = ("name",)
    filter_horizontal = ("rooms",)
