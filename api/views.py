
from rest_framework.viewsets import GenericViewSet

from photos.models import Photo

from rest_framework import mixins

from api.serializers import PhotoSerializer


# Create your views here.
class PhotoViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
