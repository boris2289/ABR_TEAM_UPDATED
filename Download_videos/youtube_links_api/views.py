from rest_framework import generics
from rest_framework.authtoken.admin import User
from .models import YouTubeLink
from .serializers import YouTubeLinkSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "You have access to this protected API!"})


class ProtectedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "JWT Authentication successful!"})


class YouTubeLinkListCreate(generics.ListCreateAPIView):
    queryset = YouTubeLink.objects.all()
    serializer_class = YouTubeLinkSerializer


class YouTubeLinkDelete(generics.DestroyAPIView):
    queryset = YouTubeLink.objects.all()
    serializer_class = YouTubeLinkSerializer


class UserRegistrationView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        print('!!"', users)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)