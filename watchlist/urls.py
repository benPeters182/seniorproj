from django.urls import path

from . import views

app_name = 'watchlist'
urlpatterns = [
    path('<list_name>/movies', views.movie_index, name='movie_index'),
    path('<list_name>/shows', views.show_index, name='show_index'),
    path('<list_name>/actors', views.actor_index, name='actor_index'),

    path('<int:movie_id>/movie-details', views.movie_detail, name='movie_detail'),
    path('<int:show_id>/show-details', views.show_detail, name='show_detail'),
    path('<int:actor_id>/actor-details', views.actor_detail, name='actor_detail'),

    path('<int:movie_id>/movie-cast', views.movie_cast, name='movie_cast'),
    path('<int:show_id>/show-cast', views.show_cast, name='show_cast'),

    path('movie-options/<list_name>/<search_text>', views.new_movie_options, name='new_movie_options'),
    path('show-options/<list_name>/<search_text>', views.new_show_options, name='new_show_options')
]
