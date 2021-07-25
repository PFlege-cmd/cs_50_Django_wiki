from django.urls import path, re_path
import re

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/random", views.getRandomPage, name="random"),
    re_path(r"wiki/search", views.search, name = "search"),
    re_path(r"wiki/new_page", views.createPage, name = "new"),
    re_path(r"wiki/(?P<site>[\w]+)$", views.get_entry, name = "test"),
    re_path(r"wiki/(?P<site>[\w]+)$", views.error, name = "error"),
    re_path(r"wiki/(?P<site>[\w]+)/edit$", views.editPage, name = "edit")
    ]