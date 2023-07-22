from django.db import models
from django.contrib.auth.models import AbstractUser

from autoslug import AutoSlugField

from .common.models import BaseModelWithUID
from .choices import UserRole, FileExtension, UserGender
from .managers import CustomUserManager
from .utils import get_file_path


class User(AbstractUser, BaseModelWithUID):
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True, db_index=True
    )
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.USER)
    gender = models.CharField(
        max_length=20, blank=True, null=True, choices=UserGender.choices, db_index=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class MyDocument(BaseModelWithUID):
    fileitem = models.FileField(upload_to=get_file_path)
    filesize = models.PositiveIntegerField(default=0)
    extension = models.CharField(max_length=20, choices=FileExtension.choices)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey("documentio.User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"User UID: {self.user.uid}, EMAIL: {self.user.email}"

class DocumentShare(BaseModelWithUID):
    sender = models.ForeignKey("documentio.User", on_delete=models.CASCADE, related_name="document_share")
    receiver = models.ForeignKey("documentio.User", on_delete=models.CASCADE)
    fileitem = models.ForeignKey("documentio.MyDocument", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Sender UID: {self.sender.uid}, Receiver UID: {self.receiver.uid}"