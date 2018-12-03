import random

from django.db.models import Count, Case, When
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from cafes.models import Cafe, CafePhoto
from core.api.utils import MultipartJsonParser
from .serializers import CafeRetrieveListSerializer, CafeCreateUpdateSerializer
from rest_framework import viewsets, status


class CafeViewSet(viewsets.ModelViewSet):
    parser_classes = (MultipartJsonParser,)

    # https://stackoverflow.com/a/22755648
    def get_serializer_class(self):
        if self.action in ('update', 'create'):
            return CafeCreateUpdateSerializer
        else:
            return CafeRetrieveListSerializer

    def get_queryset(self):
        queryset = Cafe.objects \
            .prefetch_related('photos') \
            .prefetch_related('coffeemeeting_set') \
            .annotate(num_meetings=Count('coffeemeeting', distinct=True)) \
            .select_related('uploader') \
            .select_related('last_modifier') \
            .all()

        # query string
        sorting = self.request.query_params.get('sorting', None)
        if sorting is None:
            raise ValidationError("쿼리스트링 sorting이 제공되지 않았습니다.")
        # query string에 따라 분기하여 결과를 리턴한
        elif sorting == 'popularity':
            return queryset.order_by('-num_meetings')
        elif sorting == 'recent':
            return queryset.order_by('-created')
        elif sorting == 'photo':
            return queryset.annotate(num_photo=Count('photos', distinct=True)).order_by('-num_photo')
        elif sorting == 'random':
            cafe_id_list = list(Cafe.objects.values_list('id', flat=True))
            random.shuffle(cafe_id_list)
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(cafe_id_list)])
            return queryset.order_by(preserved)
        else:
            raise ValidationError("잘못된 쿼리스트링이 전달되었습니다.")
        return queryset

    def create(self, request, *args, **kwargs):
        # Serializer는 photos를 이해하지 못하므로 미리 뺀다
        photos = request.data.pop("photos")

        # Cafe를 만든다
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cafe = serializer.save()  # perform_create은 instance를 반환하지 않는다

        # 생성한 cafe로 CafePhoto를 만든다
        for photo in photos:
            CafePhoto.objects.create(cafe=cafe, image=photo)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
