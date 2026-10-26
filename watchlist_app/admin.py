from django.contrib import admin

from watchlist_app.models import Movie, StreamPlatform, WatchList, Review

# Register your models here.
admin.site.register([Movie, WatchList, StreamPlatform, Review])
