from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from .serializer import UserSerializer, CustomJWTSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


class LoginView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
