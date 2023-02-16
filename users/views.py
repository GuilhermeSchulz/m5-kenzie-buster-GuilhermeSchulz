from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from .serializer import (
    UserSerializer,
    CustomJWTSerializer,
    UserSpecificEditSerializer,
    UserSpecificSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User

# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


class LoginView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class UserSpecificView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, user_id):
        serializer = UserSpecificSerializer(
            data=request.data, context={"request": request, "user_id": user_id}
        )
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        user_infos = User.objects.get(id=user_id)
        serializer = UserSpecificEditSerializer(
            user_infos,
            data=request.data,
            context={"request": request, "user_id": user_id},
        )
        if serializer.is_valid():
            user = serializer.update(
                User.objects.get(pk=user_id), serializer.validated_data
            )
            return Response(
                UserSpecificSerializer(user).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
