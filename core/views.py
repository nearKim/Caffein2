from django.http import Http404
from django.shortcuts import render, redirect

from core.models import FeedPhoto, MeetingPhoto, OperationScheme
from meetings.models import CoffeeMeeting, OfficialMeeting, CoffeeEducation
from partners.models import Partner
from partners.views import PartnerDetailView
from photo_albums.models import Photo


def entrypoint(request):
    """ 루트 url을 통해 처음 사이트로 들어온 경우 로그인 여부에 따라 분기한다."""
    if request.user.is_authenticated:
        # 사용자가 로그인상태인 경우
        if request.method == 'GET':
            official_meetings = OfficialMeeting.objects \
                                    .select_related('author') \
                                    .prefetch_related('photos') \
                                    .prefetch_related('participants') \
                                    .all() \
                                    .order_by('-created')[:3]
            coffee_educations = CoffeeEducation.objects \
                                    .select_related('author') \
                                    .prefetch_related('photos') \
                                    .prefetch_related('participants') \
                                    .all() \
                                    .order_by('-created')[:3]
            # 커모 중 최신 인스턴스 3개와 Photo 인스턴스 중 최신 9개를 가져온다.
            coffee_meetings = CoffeeMeeting.objects \
                                  .select_related('cafe') \
                                  .select_related('author') \
                                  .prefetch_related('photos') \
                                  .prefetch_related('participants') \
                                  .all() \
                                  .order_by('-meeting_date')[:4]
            latest_feedphotos = FeedPhoto.objects.all().order_by('-created')
            latest_albumphotos = Photo.objects.all().order_by('-created')

            # https://stackoverflow.com/a/11635996
            latest_photos = list(latest_albumphotos) + list(latest_feedphotos)
            latest_photos_sorted = sorted(latest_photos, key=lambda x: x.created, reverse=True)[:8]
            current_os = OperationScheme.latest()

            # 최근의 짝지 객체를 갖고와서 아래짝지가 몇명인지 반환하고 기본 context를 정의한다.
            latest_partner = Partner.related_partner_user(request.user)

            context = {'user': request.user,
                       'official_meetings': official_meetings,
                       'coffee_educations': coffee_educations,
                       'coffee_meetings': coffee_meetings,
                       'latest_photos': latest_photos_sorted
                       }

            # latest_partner가 존재하고 이번 학기/년도와 짝지 학기/년도가 일치하면 최신의 짝지가 존재하는 것이다.
            if latest_partner is not None and ((current_os.current_year == latest_partner.partner_year) and
                                               (current_os.current_semester == latest_partner.partner_semester)):

                # 현재 사용자가 위짝지 여부, 아래짝지 명수, 각 아래짝지의 User객체를 넣어준다
                up_partner = latest_partner.up_partner.user
                down_num = latest_partner.down_partner_count()
                if down_num == 1:
                    down_partners = [latest_partner.down_partner_1.user]
                elif down_num == 2:
                    down_partners = [latest_partner.down_partner_1.user,
                                     latest_partner.down_partner_2.user]
                elif down_num == 3:
                    down_partners = [latest_partner.down_partner_1.user,
                                     latest_partner.down_partner_2.user,
                                     latest_partner.down_partner_3.user]

                context['partner_set'] = True
                context['is_up'] = up_partner == request.user
                context['down_num'] = down_num
                context['up_partner'] = up_partner
                context['down_partners'] = down_partners
                context['score'] = latest_partner.score

                return render(request, 'accounts/index.html', context)
            else:
                # 짝지 객체가 아예 없거나 현재 학기, 년도에 해당하는 짝지가 없다면 명시적으로 아직이라고 템플릿에 전달한다.
                return render(request, 'accounts/index.html', {'user': request.user,
                                                               'partner_set': False,
                                                               'coffee_meetings': coffee_meetings,
                                                               'latest_photos': latest_photos_sorted})

    else:
        # 사용자가 인증되지 않았으면 index로 보낸다
        return redirect('core:index')
