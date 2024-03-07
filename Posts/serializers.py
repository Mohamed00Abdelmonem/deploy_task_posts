from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User


#___________________________________________________________________________________
class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    liked_usernames = serializers.SerializerMethodField()
    liked_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'image', 'created_at', 'liked_usernames', 'liked_count']

    def get_liked_usernames(self, obj):
        return [like.username for like in obj.likes.all()] 
     
    def get_liked_count(self, obj):
        return obj.likes.all().count() 
    
    

#___________________________________________________________________________________


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at', 'user']

#___________________________________________________________________________________
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']   

# ___________________________________________________________________________________

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    liked_usernames = serializers.SerializerMethodField()
    liked_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)  # Include comments field
    new_comment_text = serializers.CharField(write_only=True, required = False)

    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'image', 'created_at', 'likes','liked_usernames', 'liked_count', 'comments', 'new_comment_text']

    def get_liked_usernames(self, obj):
        return [like.username for like in obj.likes.all()] 

    def get_liked_count(self, obj):
        return obj.likes.all().count() 


    def update(self, instance, validated_data):
        # Extract the new_comment_text and create a new comment
        new_comment_text = validated_data.pop('new_comment_text', '')
        if new_comment_text:
            Comment.objects.create(post=instance, user=self.context['request'].user, comment=new_comment_text)

        return super().update(instance, validated_data)

#___________________________________________________________________________________
        