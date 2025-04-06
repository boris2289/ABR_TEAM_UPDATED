from rest_framework import serializers
from .models import YouTubeLink, Comment, Like, Category
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'youtube_link', 'user', 'content', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'youtube_link', 'user', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        like, created = Like.objects.get_or_create(**validated_data)
        return like

class YouTubeLinkSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = YouTubeLink
        fields = ['id', 'name', 'url', 'description', 'tags', 'comments', 'likes_count', 'user']

    def get_likes_count(self, obj):
        return obj.likes.count()




class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    youtube_links = serializers.PrimaryKeyRelatedField(many=True, queryset=YouTubeLink.objects.all())

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.youtube_links.set(validated_data.get('youtube_links', instance.youtube_links.all()))
        instance.save()
        return instance
