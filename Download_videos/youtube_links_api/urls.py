from django.urls import path
from .views import YouTubeLinkListCreate, YouTubeLinkDelete
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .api_views import (
    get_youtube_links,
    add_comment,
    YouTubeLinkDetail,
    LikeView,
    add_comment
)

urlpatterns = [
    path('youtube-links/', get_youtube_links, name='youtube-links-list'),
    path('youtube-links/<int:pk>/', YouTubeLinkDetail.as_view(), name='youtube-link-detail'),
    path('comments/', add_comment, name='add-comment'),
    path('likes/', LikeView.as_view(), name='like-link'),
    path('api/youtube-links/<int:pk>/comments/', add_comment, name='add-comment'),
]

