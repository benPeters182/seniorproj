from django.contrib import admin

from .models import Movie, Show, WatchList

admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(WatchList)
