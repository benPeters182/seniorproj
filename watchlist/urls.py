from django.urls import path

from . import views

app_name = 'watchlist'
urlpatterns = [
    path('<list_name>/movies', views.movie_index, name='movie_index'),
    path('<list_name>/shows', views.show_index, name='show_index'),
    path('<int:movie_id>/movie-details', views.movie_detail, name='movie_detail'),
    path('<int:show_id>/show-details', views.show_detail, name='show_detail'),
    path('new-movie/<list_name>/', views.new_movie, name='new_movie'),
    path('movie-options/<list_name>/<search_text>', views.new_movie_options, name='new_movie_options'),
    path('show-options/<list_name>/<search_text>', views.new_show_options, name='new_show_options')
]
