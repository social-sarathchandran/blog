# views.py
from rest_framework import generics, permissions
from django.db.models import Q
from .models import BlogPost
from .serializers import BlogPostSerializer
from utils import CustomPagination, APIResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils import APIResponse
import logging
from django.contrib.auth.models import User
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class BlogPostListAPIView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by("-publication_date")
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]  # Allow anyone to view posts
    pagination_class = CustomPagination
    pagination_class.page_size = 10


class BlogPostCreateAPIView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_data = {"blog_post_id": serializer.data}
            response = APIResponse(
                message="Blog post created successfully", data=response_data
            ).build_response()
            return response
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error creating blog post: {error_message}")
            response = APIResponse(
                error=error_message,
            ).build_response()
            return response


class BlogPostDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response = APIResponse(
                data=serializer.data, message="Blog post retrieved successfully"
            )
            return response.build_response()
        except User.DoesNotExist:
            error_message = "User not found"
            response = APIResponse(error=error_message, code="user_not_found")
            return response.build_response()
        except Exception as e:
            error_message = str(e)
            response = APIResponse(error=error_message)
            return response.build_response()

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response = APIResponse(
                data=serializer.data, message="Blog post updated successfully"
            )
            return response.build_response()
        except (
            User.DoesNotExist
        ):  # Assuming User model is used and ImportError: User not found is raised
            error_message = "User not found"
            response = APIResponse(error=error_message, code="user_not_found")
            return response.build_response()
        except Exception as e:
            error_message = str(e)
            response = APIResponse(error=error_message)
            return response.build_response()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response = APIResponse(message="Blog post deleted successfully")
            return response.build_response()
        except (
            User.DoesNotExist
        ):  # Assuming User model is used and ImportError: User not found is raised
            error_message = "User not found"
            response = APIResponse(error=error_message, code="user_not_found")
            return response.build_response()
        except Exception as e:
            error_message = str(e)
            response = APIResponse(error=error_message)
            return response.build_response()


class BlogPostSearchAPIView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination  # Use your custom pagination class

    def get_queryset(self):
        query = self.request.query_params.get("q")
        if query:
            return BlogPost.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).order_by("-publication_date")
        else:
            return BlogPost.objects.none()
