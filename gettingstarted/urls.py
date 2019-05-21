from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("get_result", hello.views.get_result, name="get_result"),
    path("house_id", hello.views.house_id, name="house_id"),
    path("options_landing/house_id/", hello.views.house_id, name="house_id"),
    path("get_result/options_landing/house_id/", hello.views.house_id, name="house_id"),
    path("options_landing",hello.views.options_landing, name="options_landing"),
    path("options_landing/options_landing/",hello.views.options_landing, name="options_landing"),
    path("get_result/options_landing/",hello.views.options_landing, name="options_landing"),
    path("options_landing/back/",hello.views.index, name="index"),
    path("get_json", hello.views.get_json, name="get_json"),
    path("get_rspec", hello.views.get_rspec, name = "get_rspec"),
    path("get_netem", hello.views.get_netem, name = "get_netem"),
    path("back", hello.views.index, name="index"),

]
