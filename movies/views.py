from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from .serializer import MovieSerializer, MovieOrderSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Movie
from .permissions import EmployeeJWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):

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
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class MovieSpecificView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id).delete()
        except Movie.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, movie_id):
        authentication_classes = []
        try:
            movie = Movie.objects.get(pk=movie_id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, movie_id):
        serializer = MovieOrderSerializer(
            data=request.data, context={"request": request, "movie_id": movie_id}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
