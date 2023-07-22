from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    USER = "USER", "User"


class UserGender(models.TextChoices):
    FEMALE = "FEMALE", "Female"
    MALE = "MALE", "Male"
    OTHER = "OTHER", "Other"


class FileExtension(models.TextChoices):
    PDF = "pdf", "PDF"
    DOCX = "docx", "DOCX"
    TXT = "txt", "TXT"
