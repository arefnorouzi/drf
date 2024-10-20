from rest_framework import serializers
from .models import Post


class PostInputSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=68, required=True)

    class Meta:
        model = Post
        fields = ['title', 'description']


class PostOutputSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'author_name', 'created_at', 'updated_at']
        read_only_fields = ['author_name', 'created_at', 'updated_at']
