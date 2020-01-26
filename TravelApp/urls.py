from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('signup', views.signupUser, name="signup"),
    path('home', views.home, name="home"),
    path('suggest-city', views.suggestCity, name="suggest-city"),
    path('places/<str:city>/<int:No_days>', views.places, name="places"),
    path('hotel-details/<str:city>/<str:slug>', views.hotelDetail, name="hotel-details"),
]