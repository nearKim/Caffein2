from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from rest_framework_jwt.settings import api_settings


def index(request):
    """
    카페의 전체 리스트를 반환한다.
    API 인증처리를 위해 유저의 jwt토큰을 발급하여 함께 전달한다.
    """
    
    if request.user.is_anonymous:
        raise PermissionDenied
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    return render(request, 'frontend/cafe-list.html', context={'jwt': token})


def cafe_detail_edit(request, pk):
    """
    주어진 pk의 카페의 정보를 반환한다.
    API 인증처리를 위해 유저의 jwt 토큰을 발급하여 함께 전달한다.
    """

    if request.user.is_anonymous:
        raise PermissionDenied
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    return render(request, 'frontend/cafe-detail.html', context={'jwt': token, 'cafe_id': pk})
