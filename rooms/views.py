from django_countries import countries
from django.utils import timezone
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from . import models, forms

# from django.core.paginator import Paginator, EmptyPage
from . import models


class HomeView(ListView):
    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room


def search(request):
    # GET에 아무것도 없다! 그러면 Anywhere가 들어간다
    # get("name of input", defaultValue) 형식으로 들어가면 됨(요청) => 그럼 input의 value값을 return 함(응답)
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("bed", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)

    # form 에서 받아온 것 => 사용자가 선택한 결과
    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "super_host": super_host,
    }
    # database에서 받아온 것
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(request, "rooms/search.html", {**form, **choices})


# class HomeView의 function 버전 view
# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)

#     try:
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html", {"page": rooms})
#           템플릿에서 page.object_list로 받아주면, list를 띄어줌

#     except EmptyPage:
#         return redirect("/")


# class RoomDetail의 function 버전 view
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         context = {"room": room}
#         return render(request, "rooms/room_detail.html", context)
#     except models.Room.DoesNotExist:
#         return redirect(reverse("core:home"))
#         # raise Http404()
