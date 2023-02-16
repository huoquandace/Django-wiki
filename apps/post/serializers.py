from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "created"]

class CurrentUserPostsSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, view_name="post_detail", queryset=get_user_model().objects.all()
    )

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "posts"]
