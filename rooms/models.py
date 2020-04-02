from django.db import models
from django.urls import reverse
from core import models as core_models
from django_countries.fields import CountryField
from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item model"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# Room 안에 넣지 않고, 이렇게 빼놓는 이유는?
# User에서 그랬듯, class 안에 선택지를 넣고 charfield를 사용할 수도 있다
# 그러나 그건 관리자 수준에서의 수정이 불가능해진다
# Roomtype과 Amenity, 그리고 facility 등 방관련 요소들은 관리자 수준에서 수정하고 싶다~!
class RoomType(AbstractItem):
    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstractItem):
    """Amenity Model defintion"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility Model definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRule Model definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """Phto Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


# Create your models here.
class Room(core_models.TimeStampedModel):
    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # 집주인은 room과 연관되어 있는 정보이므로, 연결해줘야함
    # foreignkey 를 사용하면 연결할 수 있음
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    # 기본적으로, room object라고 출력되는 설정을 갖고 있음
    # 그것은,,, 바로  __str__ 떄문인뎅~!~!~!!! 두둥
    # 예쁘게 바꿔주고 싶어서, 이렇게 써줬어요^,^
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        # reviews/model.py의 Review class에 room = foreiengkey ('room')이 존재함
        # 즉, review는 room 과 연결되어 있음. 그렇다면 room또한 review를 볼 수 있음
        # self.reviews.all() 을 통해 review의 요소들을 가져오고

        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return all_ratings / len(all_reviews)
