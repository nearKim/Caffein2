from django.shortcuts import render, redirect

from partners.views import PartnerDetailView


def entrypoint(request):
    """ 루트 url을 통해 처음 사이트로 들어온 경우 로그인 여부에 따라 분기한다."""
    if request.user.is_authenticated:
        # 사용자가 로그인상태인 경우 이번학기 짝지정보를 함께 보여준다.

        # return render(request, 'accounts/index.html', context={'user': request.user})
        return PartnerDetailView.as_view()(request)
    else:
        return redirect('core:index')
