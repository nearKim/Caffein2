from django.http import Http404
from django.shortcuts import render, redirect

from core.models import FeedPhoto, MeetingPhoto, OperationScheme
from meetings.models import CoffeeMeeting
from partners.models import Partner
from partners.views import PartnerDetailView
from photo_albums.models import Photo


def entrypoint(request):
    """ 루트 url을 통해 처음 사이트로 들어온 경우 로그인 여부에 따라 분기한다."""
    if request.user.is_authenticated:
        # 사용자가 로그인상태인 경우
        if request.method == 'GET':
            # 커모 중 최신 인스턴스 3개와 Photo 인스턴스 중 최신 9개를 가져온다.
            coffee_meetings = CoffeeMeeting.objects.select_related('cafe').all().order_by('-meeting_date')[:3]
            latest_feedphotos = FeedPhoto.objects.all().order_by('-created')
            latest_albumphotos = Photo.objects.all().order_by('-created')

            # https://stackoverflow.com/a/11635996
            latest_photos = list(latest_albumphotos) + list(latest_feedphotos)
            latest_photos_sorted = sorted(latest_photos, key=lambda x: x.created, reverse=True)[:9]
            latest_partner = Partner.related_partner_user(request.user)
            current_os = OperationScheme.latest()

            # latest_partner가 존재하고 이번 학기/년도와 짝지 학기/년도가 일치하면 최신의 짝지가 존재하는 것이다.
            if latest_partner is not None and ((current_os.current_year == latest_partner.partner_year) and
                                               (current_os.current_semester == latest_partner.partner_semester)):
                return render(request, 'accounts/index.html', {'user': request.user,
                                                               'partner': latest_partner,
                                                               'coffee_meetings': coffee_meetings,
                                                               'latest_photos': latest_photos_sorted})
            else:
                # 짝지 객체가 아예 없거나 현재 학기, 년도에 해당하는 짝지가 없다면 명시적으로 None을 템플릿에 전달한다.
                return render(request, 'accounts/index.html', {'user': request.user,
                                                               'partner': None,
                                                               'coffee_meetings': coffee_meetings,
                                                               'latest_photos': latest_photos_sorted})

    else:
        # 사용자가 인증되지 않았으면 index로 보낸다
        return redirect('core:index')
