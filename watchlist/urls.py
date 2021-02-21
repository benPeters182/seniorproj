from django.urls import path

from . import views

app_name = 'watchlist'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('new-movie', views.new_movie, name='new_movie')
]
