from rest_framework.response import Response
from rest_framework import status
from utils import APIResponse
from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "publication_date", "author"]

    def validate(self, data):
        try:
            # Check if the required fields are present in the data
            required_fields = ["title", "content"]
            for field in required_fields:
                if field not in data:
                    error_message = f"{field} is required"
                    response = APIResponse(
                        error=error_message, status=status.HTTP_400_BAD_REQUEST
                    )
                    raise serializers.ValidationError(response.build_response())
        except Exception as e:
            error_message = f"Validation error: {e}"
            response = APIResponse(
                error=error_message, status=status.HTTP_400_BAD_REQUEST
            )
            raise serializers.ValidationError(response.build_response())

        return data
