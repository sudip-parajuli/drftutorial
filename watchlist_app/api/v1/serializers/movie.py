from rest_framework import serializers

# from watchlist_app.models import Movie
from watchlist_app.models import WatchList, StreamPlatform,Review


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=200)
#     active = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

class MovieSerializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()
    platform=serializers.StringRelatedField()
    class Meta:
        model=WatchList
        # fields=['id','name','description','active']
        # # exclude=['active']
        fields = '__all__'

    def get_status(self,obj):
        if obj.active:
            return "Movie is running successfully!"
        return "Movie Unavailable"

""" .create() and .update() methods are already provided by default"""

class StreamSerializer(serializers.ModelSerializer):
    # movies = MovieSerializer(read_only=True, many=True)
    movies= serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movie-details'
    )
    class Meta:
        model=StreamPlatform
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField()
    class Meta:
        model=Review
        fields='__all__'


# # validations
# def validate_name(self, value):
#     not_allowed_char = ['*', '#', '@', '+', '&', '%', '/', '{', '}', '[', ']']
#
#     banned_words=['bugger', 'bullshit', 'bastard', 'crap', 'dammit', 'damn',
#                   'damned', 'damn it', 'god dammit','goddammit','God damn','god damn','goddamn'
#                     'Goddamn','goddamned','goddamnit','godsdamn','hell','holy shit''horseshit',
#                   'in shit', 'nigga','nigra','Jesus Christ','shit',]
#
#     if len(value)<2 :
#         raise serializers.ValidationError("Movie name must contain at least 2 characters!")
#
#     if any(char in value for char in not_allowed_char):
#         raise serializers.ValidationError(f"Movie name must not contain {','.join(not_allowed_char)}")
#
#     if not value[0].isupper():
#         raise serializers.ValidationError("Movie name must start with capital letter.")
#
#     # if any(banned_words in value.lower() for banned_words in banned_words):
#     #     raise serializers.ValidationError("Movie name contains improper word")
#
#     if Movie.objects.filter(name__iexact=value).exists():
#         raise serializers.ValidationError("Movie with this name already exists")
#
#
#     return value
#
# def validate_description(self, value):
#
#     banned_words=['bugger', 'bullshit', 'bastard', 'crap', 'dammit', 'damn',
#                   'damned', 'damn it', 'god dammit','goddammit','God damn','god damn','goddamn'
#                     'Goddamn','goddamned','goddamnit','godsdamn','hell','holy shit''horseshit',
#                   'in shit', 'nigga','nigra','Jesus Christ','shit',]
#
#     if len(value) < 20:
#         raise serializers.ValidationError("Movie description must contain at least 20 characters!")
#
#     # if any(banned_words in value.lower() for banned_words in banned_words):
#     #     raise serializers.ValidationError("Movie description contains improper word")
#
#     return value
#
# def validate(self, attrs):
#     name=attrs.get('name')
#     description=attrs.get('description')
#     banned_words = ['bugger', 'bullshit', 'bastard', 'crap', 'dammit', 'damn',
#                     'damned', 'damn it', 'god dammit', 'goddammit', 'God damn', 'god damn', 'goddamn',                                                                    'Goddamn', 'goddamned',
#                     'goddamnit', 'godsdamn', 'hell', 'holy shit''horseshit',
#                     'in shit', 'nigga', 'nigra', 'Jesus Christ', 'shit', ]
#
#     if name.strip().lower()==description.strip().lower():
#         raise serializers.ValidationError("Movie name and Description can not be same")
#
#     for word in banned_words:
#         if word in name.strip().lower() or word in description.strip().lower():
#             raise serializers.ValidationError("Movie name or description contain improper word.")
#
#     return attrs









    