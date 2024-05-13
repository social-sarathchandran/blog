# urls.py
from django.urls import path
from .views import (
    BlogPostListAPIView,
    BlogPostCreateAPIView,
    BlogPostDetailUpdateDeleteAPIView,
    BlogPostSearchAPIView,
)

urlpatterns = [
    path("posts/", BlogPostListAPIView.as_view(), name="post-list"),
    path("posts/create/", BlogPostCreateAPIView.as_view(), name="post-create"),
    path(
        "posts/<int:pk>/",
        BlogPostDetailUpdateDeleteAPIView.as_view(),
        name="post-detail",
    ),
    path("search/", BlogPostSearchAPIView.as_view(), name="post-search"),
]
