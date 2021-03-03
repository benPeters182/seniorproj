from django.urls import path

from . import views

app_name = 'watchlist'
urlpatterns = [
    path('<list_name>', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('<list_name>/new-movie', views.new_movie, name='new_movie'),
    path('<list_name>/new-movie-options', views.new_movie, name='new_movie_options')
]
