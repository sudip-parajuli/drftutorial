"""Manual and model serializers for the internship's first Movie exercise."""
from rest_framework import serializers
from watchlist_app.models import Movie


class ManualMovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field in ('name', 'description', 'active'):
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
        return instance


class FoundationMovieSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_status(self, obj):
        return "Movie is running successfully!" if obj.active else "Not Available!"

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Movie name must contain at least 2 characters.")
        if any(char in value for char in '*#@+&%/{}[]'):
            raise serializers.ValidationError("Movie name must not contain these special characters.")
        if not value[0].isupper():
            raise serializers.ValidationError("First letter of name must be uppercase.")
        duplicates = Movie.objects.filter(name__iexact=value)
        if self.instance:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise serializers.ValidationError("Movie with this name already exists.")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Description must contain at least 10 characters.")
        return value

    def validate(self, attrs):
        name = attrs.get('name', getattr(self.instance, 'name', ''))
        description = attrs.get('description', getattr(self.instance, 'description', ''))
        if name.strip().casefold() == description.strip().casefold():
            raise serializers.ValidationError("Name and description must not be the same.")
        # Keep the original exercise's prohibited-word validation behavior.
        words = ['bastard', 'bugger', 'bullshit', 'crap', 'dammit', 'damn', 'damn it', 'damned', 'god dammit', 'god damn', 'goddammit', 'goddamn', 'goddamned', 'goddamnit', 'godsdamn', 'hell', 'holy shit', 'horseshit', 'in shit', 'jesus christ', 'nigga', 'nigra', 'shit']
        if any(word in name.casefold() or word in description.casefold() for word in words):
            raise serializers.ValidationError("Movie name or description contains improper words.")
        return attrs
