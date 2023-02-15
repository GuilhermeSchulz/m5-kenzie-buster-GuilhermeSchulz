from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from .serializer import MovieSerializer, MovieDeleteSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Movie
from .permissions import EmployeeJWTAuthentication


class MovieView(APIView):

    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = MovieSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        authentication_classes = []
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieSpecificView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id).delete()
        except Movie.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
