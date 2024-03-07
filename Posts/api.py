from django.shortcuts import render
from rest_framework import generics
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .models import Post, Comment

#___________________________________________________________________________________

# test module simple history
def post_history(request, post_id):
    post_instance = Post.objects.get(pk=post_id)
    historical_data = post_instance.history.all()

    context = {
        'post_instance': post_instance,
        'historical_data': historical_data,
    }

    return render(request, 'post_history.html', context)

# ___________________________________________________________________________________


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['caption', 'user__username']
    filterset_fields = ['user', 'created_at']
    permission_classes = [IsAuthenticated]  # Optional: This enforces that users need to be authenticated to perform CRUD operations


    def perform_create(self, serializer):
        # Set the user field explicitly to the current user making the request
        serializer.save(user=self.request.user)
   
# ___________________________________________________________________________________


class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]  # Optional: This enforces that users need to be authenticated to perform CRUD operations

                                
    def get_object(self):
        post = super().get_object()
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        post.comments = comments
        return post

# ___________________________________________________________________________________

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
