from django.urls import path
from . import views

app_name = "single_pages"

urlpatterns = [
    path("", views.index_page, name="index_page"),
    path("members/", views.members_page, name="members_page"),
    path("edu/", views.edu_page, name="edu_page"),
    path("map/", views.map_page, name="map_page"),
    path("list-no/", views.blog_list_no, name="blog_page"),
    path("list/", views.blog_list, name="blog_list"),
]
