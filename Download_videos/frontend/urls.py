from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', serve, {'document_root': settings.STATICFILES_DIRS[0], 'path': 'index.html'}, name='angular_app'),
]
