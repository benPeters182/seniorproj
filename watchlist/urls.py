from django.urls import path

from . import views

app_name = 'watchlist'
urlpatterns = [
    path('<list_name>', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('new-movie/<list_name>/', views.new_movie, name='new_movie'),
    path('movie-options/<list_name>/<search_text>', views.new_movie_options, name='new_movie_options')
]
