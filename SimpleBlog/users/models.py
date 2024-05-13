# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework_simplejwt.tokens import RefreshToken


class TimestampedModel(models.Model):
    """
    A mixin class add for 'create_date' and 'update_date'
    """

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimestampedModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "password",
    ]

    # Resolve reverse accessor name clashes for groups and user_permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        related_query_name="customuser",
        blank=True,
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        related_query_name="customuser",
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
    )

    def __str__(self):
        return self.email

    def generate_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserLoginRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.login_time}"


class UserLoginRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.login_time}"


class TokenBlacklist(TimestampedModel):
    jti = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()

    @classmethod
    def is_blacklisted(cls, jti):
        return cls.objects.filter(jti=jti).exists()

    @classmethod
    def add_to_blacklist(cls, jti, expires_at=None):
        if not expires_at:
            expires_at = timezone.now()
        cls.objects.create(jti=jti, expires_at=expires_at)


