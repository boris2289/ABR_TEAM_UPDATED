from .models import YouTubeLink, Comment, Like
from .serializers import YouTubeLinkSerializer, CommentSerializer, LikeSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import YouTubeLink, Comment
from .serializers import CommentSerializer


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_youtube_links(request):
    if request.method == 'GET':
        links = YouTubeLink.objects.filter(user=request.user)
        serializer = YouTubeLinkSerializer(links, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = YouTubeLinkSerializer(data=request.data)
        if serializer.is_valid():
            youtube_link = serializer.save(user=request.user)
            comments_data = request.data.get('comments', [])
            for comment_data in comments_data:
                comment_serializer = CommentSerializer(data=comment_data)
                if comment_serializer.is_valid():
                    comment_serializer.save(youtube_link=youtube_link, user=request.user)
                else:
                    return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_comment(request, pk):
    try:
        youtube_link = YouTubeLink.objects.get(pk=pk)
    except YouTubeLink.DoesNotExist:
        return Response({"detail": "YouTube link not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comments = Comment.objects.filter(youtube_link=youtube_link)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(youtube_link=youtube_link, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YouTubeLinkDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return YouTubeLink.objects.get(pk=pk)
        except YouTubeLink.DoesNotExist:
            raise NotFound(detail="YouTube link not found")

    def get(self, request, pk):
        youtube_link = self.get_object(pk)
        if youtube_link.user != request.user:
            return Response({"detail": "You do not have permission to view this YouTube link."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = YouTubeLinkSerializer(youtube_link)
        return Response(serializer.data)

    def delete(self, request, pk):
        youtube_link = self.get_object(pk)
        if youtube_link.user != request.user:
            return Response({"detail": "You do not have permission to delete this YouTube link."},
                            status=status.HTTP_403_FORBIDDEN)

        youtube_link.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LikeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        youtube_link_id = data.get('youtube_link')
        if not youtube_link_id:
            return Response({"detail": "YouTube link ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            youtube_link = YouTubeLink.objects.get(id=youtube_link_id)
        except YouTubeLink.DoesNotExist:
            return Response({"detail": "YouTube link not found."}, status=status.HTTP_404_NOT_FOUND)

        data['user'] = request.user.id
        data['youtube_link'] = youtube_link.id

        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            if Like.objects.filter(youtube_link=youtube_link, user=request.user).exists():
                return Response({"detail": "You have already liked this YouTube link."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
