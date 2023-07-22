from django.urls import path

from ..views.documents import (
    PrivateDocumentList,
    PrivateDocumentDetail,
    PrivateDocumentShareList,
    PrivateDocumentRecieveList,
    PrivateDocumentDownload,
)

urlpatterns = [
    path(
        "<uuid:document_uid>/download/",
        PrivateDocumentDownload.as_view(),
        name="document.download",
    ),
    path(
        "<uuid:document_uid>/", PrivateDocumentDetail.as_view(), name="document.detail"
    ),
    path("", PrivateDocumentList.as_view(), name="document.list"),
    path("share/", PrivateDocumentShareList.as_view(), name="document.share"),
    path("receive/", PrivateDocumentRecieveList.as_view(), name="document.receive"),
]
