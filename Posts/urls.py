from django.urls import path
from .api import PostListCreateView, DetailPost, post_history

urlpatterns = [
    path('posts/<int:post_id>/history/', post_history, name='post_history'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>', DetailPost.as_view(), name='detail_post'),

]           