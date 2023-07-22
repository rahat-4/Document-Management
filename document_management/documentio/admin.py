from django.contrib import admin

from .models import User, MyDocument


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["uid", "email", "role"]


@admin.register(MyDocument)
class MyDocumentAdmin(admin.ModelAdmin):
    list_display = ["uid", "title", "extension", "filesize", "_user"]

    def _user(self, obj):
        return obj.user.email
