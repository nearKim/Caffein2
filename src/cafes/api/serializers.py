from rest_framework import serializers

from accounts.api.serializers import CafeUploaderSerializer
from cafes.models import CafePhoto, Cafe


class CafePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafePhoto
        fields = ('image',)


class CafeRetrieveListSerializer(serializers.ModelSerializer):
    uploader = CafeUploaderSerializer()
    last_modifier = CafeUploaderSerializer()
    photos = CafePhotoSerializer(many=True)
    price = serializers.SerializerMethodField()
    closed_day = serializers.SerializerMethodField()

    class Meta:
        model = Cafe
        fields = '__all__'

    def get_price(self, obj):
        return obj.get_price_display()

    def get_closed_day(self, obj):
        return obj.get_closed_day_display()


class CafeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = '__all__'
