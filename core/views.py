from django.shortcuts import render


# Home view for anonymous users

def index(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/index.html', context={'user': request.user})
    else:
        return render(request, 'index.html')


# Comment Views


