from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


# 카페 API에서 사용할 업로더/마지막 수정자 전용 serializer
class CafeUploaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # 개인정보 보호를 위해 필요한 필드만 넣어준다.
        fields = ('name', 'profile_pic', 'is_staff')
