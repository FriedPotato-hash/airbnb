from django.contrib import admin
from django.utils.html import mark_safe
from . import models


# @admin.register(models.RoomType)
# class ItemAdmin(admin.ModelAdmin):
#     """ Item Admin Definition"""

#     pass


# @admin.register(models.Amenity)
# class ItemAdmin(admin.ModelAdmin):
#     """ Item Admin Definition"""

#     pass


# @admin.register(models.Facility)
# class ItemAdmin(admin.ModelAdmin):
#     """ Item Admin Definition"""

#     pass


# @admin.register(models.HouseRule)
# class ItemAdmin(admin.ModelAdmin):
#     """ Item Admin Definition"""

#     pass


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition"""

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths",)},),
        (
            "More about Rooms",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules",),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = ("name", "price", "bedrooms")

    list_filter = (
        "instant_book",
        "city",
        "country",
    )

    raw_id_fileds = ("hosts",)

    search_fields = ("city",)
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # manytomany에 속하는 항목들은 (amenities, facilities, house_rules)
    # admin channel에 위와 같이 list_display에 띄울 수 없다.
    # 따라서 관련 함수를 만들어 줘야한당
    # class안의 self는 class 그 자체를 받고, obj는 해당 row(행)을 받는다
    # 해당 함수의 결과 또한 rooms admin에 띄어진다
    def count_amenities(self, obj):
        return obj.amenities.count()
        # return obj 하면 __str__때문에, room name이 filterdisplay에 뜬다

    # 줄여서 쓸 수 있다(filter display를)
    count_amenities.short_description = "count_amenities"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "count_photos"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width = 50px src = "{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"
