from django.shortcuts import render, redirect


def entrypoint(request):
    """ 루트 url을 통해 처음 사이트로 들어온 경우 로그인 여부에 따라 분기한다."""
    if request.user.is_authenticated:
        return render(request, 'accounts/index.html', context={'user': request.user})
    else:
        return redirect('core:index')
