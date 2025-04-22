from rest_framework import serializers
from .models import YouTubeLink, Comment, Like, Category
from django.contrib.auth.models import User


class LikeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    youtube_link = serializers.URLField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        like, created = Like.objects.get_or_create(**validated_data)
        return like


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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'youtube_link', 'user', 'content', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class YouTubeLinkSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = YouTubeLink
        fields = ['id', 'name', 'url', 'description', 'tags', 'comments', 'likes_count', 'user']

    def get_likes_count(self, obj):
        return obj.likes.count()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

