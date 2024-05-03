from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # PARSER
    path("parse", views.parse_csv),

    # QUERIES
    path("all", views.get_all_records),
    path("towns", views.get_towns),
    path("industries", views.get_industries),
    path("main_tiers", views.get_main_tiers),
    path("sub_tiers", views.get_sub_tiers),

    # SEARCH
    path("search", views.search_field)
]