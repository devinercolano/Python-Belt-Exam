from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^register$', views.register, name="register"),
    url(r'^createQuote$', views.createQuote, name='createQuote'),
    url(r'^returnQuotes$', views.returnQuotes, name='returnQuotes'),
    url(r'^users/(?P<id>\d+)$', views.showUser, name='showUser'),
    url(r'^addFavorite/(?P<id>\d+)$', views.addFavorite, name='addFavorite'),
    url(r'^removeFavorite/(?P<id>\d+)$', views.removeFavorite, name='removeFavorite'),
]