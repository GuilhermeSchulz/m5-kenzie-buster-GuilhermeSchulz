from rest_framework import serializers
from .models import Movie, Ratings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    synopsis = serializers.CharField(required=False)
    rating = serializers.ChoiceField(
        choices=Ratings, required=False, default=Ratings.GRATING
    )
    duration = serializers.CharField(required=False)
    added_by = serializers.CharField(read_only=True)
    added_by = serializers.SerializerMethodField()

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        movie = Movie.objects.create(**validated_data)
        return movie

    class Meta:
        model = Movie
        fields = ["id", "title", "duration", "rating", "synopsis", "added_by"]
        read_only_fields = ("id", "added_by")

    def get_added_by(self, obj):
        return obj.user.email


class MovieDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
