from rest_framework import serializers

from accounts.api.serializers import CafeUploaderSerializer
from cafes.models import CafePhoto, Cafe


class CafePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafePhoto
        fields = ('image', 'cafe')


class CafeRetrieveListSerializer(serializers.ModelSerializer):
    uploader = CafeUploaderSerializer()
    last_modifier = CafeUploaderSerializer()
    photos = CafePhotoSerializer(many=True)

    class Meta:
        model = Cafe
        fields = '__all__'


class CafeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = '__all__'



