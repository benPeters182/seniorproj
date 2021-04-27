from django.contrib import admin

from .models import Movie, Show, WatchList, Actor, Role

admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(WatchList)
admin.site.register(Actor)
admin.site.register(Role)
