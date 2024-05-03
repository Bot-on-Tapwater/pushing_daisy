from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # QUERIES
    path("all", views.get_all_records),
    path("towns", views.get_towns),
    path("industries", views.get_industries),
]