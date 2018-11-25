from rest_framework.response import Response

from cafes.models import Cafe, CafePhoto
from core.api.utils import MultipartJsonParser
from .serializers import CafeRetrieveListSerializer, CafePhotoSerializer, CafeCreateUpdateSerializer
from rest_framework import viewsets


class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all()
    parser_classes = (MultipartJsonParser,)

    # https://stackoverflow.com/a/22755648
    def get_serializer_class(self):
        if self.action in ('update', 'create'):
            return CafeCreateUpdateSerializer
        else:
            return CafeRetrieveListSerializer

    def update(self, request, *args, **kwargs):
        # Patch도 그냥 Put으로 통합한다
        partial = True
        instance = self.get_object()

        # request로 넘어온 photos form data를 뽑아내어 생성한다.
        for photo in request.data.pop("photos"):
            CafePhoto.objects.create(cafe=instance, image=photo)

        # 나머지 데이터는 그대로 serializer에 넣어준다
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
