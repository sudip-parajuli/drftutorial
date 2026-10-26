from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class MovieSerializer(serializers.ModelSerializer):
    """Existing watchlist representation; the historical name is retained."""
    status = serializers.SerializerMethodField()
    platform = serializers.StringRelatedField()
    platform_id = serializers.PrimaryKeyRelatedField(
        source="platform", queryset=StreamPlatform.objects.all(),
        write_only=True, required=False, allow_null=True,
    )

    class Meta:
        model = WatchList
        fields = '__all__'

    def get_status(self, obj):
        return "Movie is running successfully!" if obj.active else "Movie Unavailable"


class StreamSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='movie-details',
    )

    class Meta:
        model = StreamPlatform
        fields = '__all__'


class NestedStreamSerializer(serializers.ModelSerializer):
    """Nested relationship exercise imported from RESTFrameworkTutorial."""
    movies = MovieSerializer(read_only=True, many=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
