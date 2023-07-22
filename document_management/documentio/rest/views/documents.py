from django.http import HttpResponse

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import filters

from documentio.models import MyDocument, DocumentShare

from ..serializers.documents import (
    PrivateDocumentListSerializer,
    PrivateDocumentDetailSerializer,
    PrivateDocumentShareListSerializer,
    PrivateDocumentRecieveListSerializer,
    PrivateDocumentDownloadSerializer,
)


class PrivateDocumentList(ListCreateAPIView):
    queryset = MyDocument.objects.filter()
    serializer_class = PrivateDocumentListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
        "description",
        "extension",
        "created_at__date",
    ]

    def get_queryset(self):
        queryset = self.queryset.select_related("user").filter(user=self.request.user)

        return queryset


class PrivateDocumentDetail(RetrieveUpdateDestroyAPIView):
    queryset = MyDocument.objects.filter()
    serializer_class = PrivateDocumentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        document_uid = self.kwargs.get("document_uid", None)

        try:
            my_document = MyDocument.objects.get(
                uid=document_uid, user=self.request.user
            )
        except:
            raise ValidationError({"detail": "Document not found!"})

        return my_document


class PrivateDocumentShareList(ListCreateAPIView):
    queryset = DocumentShare.objects.filter()
    serializer_class = PrivateDocumentShareListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(sender=self.request.user)

        return queryset


class PrivateDocumentRecieveList(ListAPIView):
    queryset = DocumentShare.objects.filter()
    serializer_class = PrivateDocumentRecieveListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(receiver=self.request.user)

        return queryset


class PrivateDocumentDownload(RetrieveAPIView):
    queryset = MyDocument.objects.filter()
    serializer_class = PrivateDocumentDownloadSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        document_uid = kwargs.get("document_uid")

        try:
            document = MyDocument.objects.get(uid=document_uid, user=self.request.user)
        except:
            raise ValidationError({"detail": "File not found!"})

        content_types = {
            "pdf": "application/pdf",
            "txt": "text/plain",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }

        extension = document.extension.lower()

        content_type = content_types.get(extension, "application/octet-stream")

        response = HttpResponse(document.fileitem, content_type=content_type)
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{document.fileitem.name}"'

        return response
