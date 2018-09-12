from django.http import HttpResponseForbidden
from django.shortcuts import render


def logged_in(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/index.html', context={'user': request.user})
    else:
        return HttpResponseForbidden

# def index(request):
#     if request.user.is_authenticated:
#         return render(request, 'accounts/index.html', context={'user': request.user})
#     else:
#         return render(request, 'index.html')
