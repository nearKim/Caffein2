from django.http import Http404
from django.shortcuts import render, redirect

from core.models import FeedPhoto, MeetingPhoto, OperationScheme, Meeting
from meetings.models import CoffeeMeeting, OfficialMeeting, CoffeeEducation
from partners.models import Partner, PartnerMeeting
from partners.views import PartnerDetailView
from photo_albums.models import Photo


def entrypoint(request):
    """ 루트 url을 통해 처음 사이트로 들어온 경우 로그인 여부에 따라 분기한다."""
    if request.user.is_authenticated:
        # 사용자가 로그인상태인 경우
        if request.method == 'GET':
            # Meeting 객체들을 모두 불러와서 그 중 커모에 해당하는 객체는 빼준다.
            every_coffee_meetings = CoffeeMeeting.objects.all().values('meeting_ptr')
            official_and_educations = Meeting.objects \
                                          .select_related('author') \
                                          .select_related('officialmeeting') \
                                          .select_related('coffeeeducation') \
                                          .exclude(id__in=every_coffee_meetings) \
                                          .order_by('-created')[:3]

            # 커모 중 최신 인스턴스 4개를 가져온다.
            coffee_meetings = CoffeeMeeting.objects \
                                  .select_related('cafe') \
                                  .select_related('author') \
                                  .prefetch_related('photos') \
                                  .prefetch_related('participants') \
                                  .prefetch_related('cafe__photos') \
                                  .all() \
                                  .order_by('-meeting_date')[:4]

            # 짝모 역시 최신 인스턴스 4개를 가져온다
            latest_partnermeetings = PartnerMeeting.objects \
                                         .select_related('author') \
                                         .select_related('partner') \
                                         .select_related('partner__up_partner__user') \
                                         .prefetch_related('photos') \
                                         .all().order_by('-created')[:4]

            # 사진첩 carousel은 photo_album의 사진들만 8개까지 보여준다.
            latest_albumphotos = Photo.objects.all().order_by('-created')[:8]

            current_os = OperationScheme.latest()

            # 최근의 짝지 객체를 갖고와서 아래짝지가 몇명인지 반환하고 기본 context를 정의한다.
            latest_partner = Partner.related_partner_user(request.user)

            context = {'user': request.user,
                       'official_meetings': official_and_educations,
                       'coffee_meetings': coffee_meetings,
                       'partner_meetings': latest_partnermeetings,
                       'latest_photos': latest_albumphotos
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
                context['partner_set'] = False
                return render(request, 'accounts/index.html', context)

    else:
        # 사용자가 인증되지 않았으면 index로 보낸다
        return redirect('core:index')


def developer(request):
    if request.method == 'GET':
        return render(request, 'core/developers.html')
