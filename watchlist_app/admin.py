from django.contrib import admin

# from watchlist_app.models import Movie
from watchlist_app.models import StreamPlatform,WatchList,Review

# Register your models here.
admin.site.register([WatchList,StreamPlatform,Review])
