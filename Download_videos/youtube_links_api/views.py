from rest_framework import generics
from .models import YouTubeLink
from .serializers import YouTubeLinkSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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
