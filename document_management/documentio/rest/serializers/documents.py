import PyPDF2
import docx

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from documentio.common.serializers import UserSlimSerializer, DocumentSlimSerializer
from documentio.choices import FileExtension
from documentio.models import User, MyDocument, DocumentShare


class PrivateDocumentListSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()
    format = serializers.CharField(source="extension", read_only=True)
    upload_date = serializers.SerializerMethodField()

    class Meta:
        model = MyDocument
        fields = [
            "uid",
            "fileitem",
            "title",
            "description",
            "file_size",
            "format",
            "upload_date",
        ]

        read_only_fields = [
            "uid",
            "title",
            "description",
            "file_size",
            "format",
            "upload_date",
        ]

    def get_file_size(self, obj):
        return f"{obj.filesize} bytes"

    def get_upload_date(self, obj):
        return obj.created_at.date()

    def create(self, validated_data):
        user = self.context["request"].user
        fileitem = validated_data.get("fileitem", None)

        if fileitem:
            extension = fileitem.name.split(".")[-1]

            if extension not in [extension[0] for extension in FileExtension.choices]:
                raise ValidationError(
                    {"detail": f"{extension.upper()} format is not allowed for upload!"}
                )

            max_size = 5 * 1024 * 1024
            if fileitem.size > max_size:
                raise ValidationError({"detail": "File size should not exceed 5 MB!"})

            if extension == FileExtension.TXT:
                title = fileitem.name.split(".")[0]
                description = fileitem.read().decode("utf-8")

                my_document = MyDocument.objects.create(
                    filesize=fileitem.size,
                    extension=FileExtension.TXT,
                    title=title,
                    description=description,
                    user=user,
                    **validated_data,
                )

            if extension == FileExtension.PDF:
                title = fileitem.name.split(".")[0]
                description = ""

                with fileitem.open(mode="rb") as file:
                    pdfs = PyPDF2.PdfReader(file)

                    for page_number in range(len(pdfs.pages)):
                        page = pdfs.pages[page_number]
                        description += page.extract_text()

                    my_document = MyDocument.objects.create(
                        filesize=fileitem.size,
                        extension=FileExtension.PDF,
                        title=title,
                        description=description,
                        user=user,
                        **validated_data,
                    )

            if extension == FileExtension.DOCX:
                title = fileitem.name.split(".")[0]
                description = ""

                with fileitem.open(mode="rb") as file:
                    docs = docx.Document(file)

                    for doc in docs.paragraphs:
                        description += doc.text + "\n"

                    my_document = MyDocument.objects.create(
                        filesize=fileitem.size,
                        extension=FileExtension.PDF,
                        title=title,
                        description=description,
                        user=user,
                        **validated_data,
                    )

        return my_document


class PrivateDocumentDetailSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()
    format = serializers.CharField(source="extension")
    upload_date = serializers.SerializerMethodField()

    class Meta:
        model = MyDocument
        fields = [
            "fileitem",
            "title",
            "description",
            "file_size",
            "format",
            "upload_date",
        ]
        read_only_fields = ["fileitem", "title", "file_size", "format", "upload_date"]

    def get_file_size(self, obj):
        return f"{obj.filesize} bytes"

    def get_upload_date(self, obj):
        return obj.created_at.date()

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)

        return super().update(instance, validated_data)


class PrivateDocumentShareListSerializer(serializers.ModelSerializer):
    receiver_user = UserSlimSerializer(source="receiver", read_only=True)
    receiver = serializers.SlugRelatedField(
        queryset=User.objects.filter(), slug_field="uid", write_only=True
    )
    fileitem = serializers.SlugRelatedField(
        queryset=MyDocument.objects.filter(), slug_field="uid", write_only=True
    )
    file_item = DocumentSlimSerializer(source="fileitem", read_only=True)

    class Meta:
        model = DocumentShare
        fields = ["uid", "receiver", "fileitem", "receiver_user", "file_item"]

    def create(self, validated_data):
        user = self.context["request"].user

        documtent_share = DocumentShare.objects.create(sender=user, **validated_data)

        return documtent_share


class PrivateDocumentRecieveListSerializer(serializers.ModelSerializer):
    sender_user = UserSlimSerializer(source="sender", read_only=True)
    file_item = DocumentSlimSerializer(source="fileitem", read_only=True)

    class Meta:
        model = DocumentShare
        fields = ["uid", "sender_user", "file_item"]


class PrivateDocumentDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDocument
        fields = ["fileitem"]
