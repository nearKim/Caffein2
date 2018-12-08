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
    created = serializers.DateTimeField(format="%Y년 %m월 %d일")
    modified = serializers.DateTimeField(format="%Y년 %m월 %d일")
    from_time = serializers.TimeField(format="%I:%M %p")
    to_time = serializers.TimeField(format="%I:%M %p")

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
