from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.test, name="index"),
    path('login', views.login, name="post_login"),
    # path('increment_like', views.increment_like, name="post_increment_like"),
    # path('save_activity', views.save_activity, name="post_save_activity"),
    path('bored_clicked', views.bored_clicked, name="bored_clicked"),

    # path('random_activity', views.random_activity, name="get_random_activity"),
    path('saved_list', views.saved_list, name="get_saved_list"),
]
