from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from rest_framework_jwt.settings import api_settings


# Create your views here.
def index(request):
    if request.user.is_anonymous:
        raise PermissionDenied
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    return render(request, 'frontend/cafe.html', context={'jwt': token})
