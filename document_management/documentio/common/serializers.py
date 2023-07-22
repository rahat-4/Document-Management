from rest_framework import serializers

from documentio.models import User, MyDocument

class UserSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "email", "first_name", "last_name", "gender", "date_of_birth", "role"]
        read_only_fields = ["__all__"]

class DocumentSlimSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()
    format = serializers.CharField(source="extension", read_only=True)
    upload_date = serializers.SerializerMethodField()

    class Meta:
        model = MyDocument
        fields = ["uid", "fileitem", "title", "description", "file_size", "format", "upload_date"]
        read_only_fields = ["__all__"]
    
    def get_file_size(self, obj):
        return f"{obj.filesize} bytes"

    def get_upload_date(self, obj):
        return obj.created_at.date()