from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormMixin
)

from accounts.models import ActiveUser
from cafes.models import Cafe, CafePhoto
from comments.forms import CommentForm
from core.mixins import FaceBookPostMixin, StaffRequiredMixin, ValidAuthorRequiredMixin
from meetings.mixins import OfficialMeetingCreateUpdateMixin, CoffeeEducationCreateUpdateMixin, \
    CoffeeMeetingCreateUpdateMixin

from core.models import OperationScheme
from .models import (
    OfficialMeeting,
    CoffeeEducation,
    CoffeeMeeting)
from core.models import Meeting, MeetingPhoto


# TODO: 정리하기
# 공식 모임과 커피교육을 한 화면에 보여주는 ListView
class OfficialAndEducationListView(LoginRequiredMixin, ListView):
    template_name = 'meetings/meeting_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OfficialAndEducationListView, self).get_context_data(**kwargs)
        context['coffee_education_list'] = CoffeeEducation.objects \
            .select_related('author') \
            .all() \
            .order_by('-created')
        return context

    def get_queryset(self):
        queryset = OfficialMeeting.objects \
            .select_related('author') \
            .all() \
            .order_by('-created')
        return queryset


# CRUD for OfficialMeeting

class OfficialMeetingCreateView(StaffRequiredMixin, FaceBookPostMixin, OfficialMeetingCreateUpdateMixin, CreateView):
    def form_valid(self, form):
        instance = form.save()
        self.message = '{}님이 공식모임을 생성하였습니다. 아래 링크에서 확인해주세요!'.format(self.request.user.name)
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhoto(meeting=instance, image=f)
                photo.save()
        return super(OfficialMeetingCreateView, self).form_valid(form)


class OfficialMeetingUpdateView(StaffRequiredMixin, OfficialMeetingCreateUpdateMixin, UpdateView):
    def get_success_url(self, **kwargs):
        return reverse_lazy('meetings:official-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        instance = form.save()
        MeetingPhoto.objects.filter(meeting=instance).delete()

        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhoto(meeting=instance, image=f)
                photo.save()

        return super(OfficialMeetingUpdateView, self).form_valid(form)


class OfficialMeetingListView(LoginRequiredMixin, ListView):
    model = OfficialMeeting


class OfficialMeetingDetailView(LoginRequiredMixin, FormMixin, DetailView):
    form_class = CommentForm
    queryset = OfficialMeeting.objects \
        .prefetch_related('participants') \
        .prefetch_related('participants__user') \
        .prefetch_related('comments__author') \
        .select_related('author')

    def get_context_data(self, **kwargs):
        context = super(OfficialMeetingDetailView, self).get_context_data()
        context['user'] = self.request.user
        context['participated'] = True if ActiveUser.objects.filter(
            user=self.request.user).latest() in self.object.participants.all() else False
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context


# CoffeeEducation
class CoffeeEducationCreateView(StaffRequiredMixin, FaceBookPostMixin, CoffeeEducationCreateUpdateMixin, CreateView):

    def form_valid(self, form):
        instance = form.save()
        self.message = '{}님이 커피교육을 열었습니다. 아래 링크에서 확인해주세요!'.format(self.request.user.name)
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhoto(meeting=instance, image=f)
                photo.save()
        return super(CoffeeEducationCreateView, self).form_valid(form)


class CoffeeEducationUpdateView(StaffRequiredMixin, CoffeeEducationCreateUpdateMixin, UpdateView):
    def get_success_url(self, **kwargs):
        return reverse_lazy('meetings:education-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        instance = form.save()
        MeetingPhoto.objects.filter(meeting=instance).delete()

        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhoto(meeting=instance, image=f)
                photo.save()

        return super(CoffeeEducationUpdateView, self).form_valid(form)


class CoffeeEducationListView(LoginRequiredMixin, ListView):
    model = CoffeeEducation


class CoffeeEducationDetailView(LoginRequiredMixin, FormMixin, DetailView):
    form_class = CommentForm
    queryset = CoffeeEducation.objects \
        .prefetch_related('participants') \
        .prefetch_related('participants__user') \
        .prefetch_related('comments__author') \
        .select_related('author')

    def get_context_data(self, **kwargs):
        context = super(CoffeeEducationDetailView, self).get_context_data()
        context['user'] = self.request.user
        context['participated'] = True if ActiveUser.objects.filter(
            user=self.request.user).latest() in self.object.participants.all() else False
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context


# CoffeeMeeting
class CoffeeMeetingCreateView(LoginRequiredMixin, FaceBookPostMixin, CoffeeMeetingCreateUpdateMixin, CreateView):
    def dispatch(self, request, *args, **kwargs):
        self.cafe = get_object_or_404(Cafe, pk=self.kwargs['pk'])

        latest_active_user = ActiveUser.objects.filter(user=request.user).latest()
        latest_os = OperationScheme.latest()
        # 이번 년도,학기와 가장 마지막 등록한 activeuser의 등록 년도,학기가 일치해야 커모를 열 수 있다.
        # 그게 아니라면 예전에 등록하고 이번에는 등록하지 않은 회원인 것이다.
        if not (latest_os.current_year == latest_active_user.active_year and
                latest_os.current_semester == latest_active_user.active_semester):
            raise PermissionDenied('활동회원으로 등록하셔야 커모를 열 수 있습니다.')
        return super(CoffeeMeetingCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super(CoffeeMeetingCreateView, self).get_form_kwargs()
        form_kwargs['request'] = self.request
        form_kwargs['cafes'] = self.cafe
        form_kwargs['read_only'] = True
        return form_kwargs

    def form_valid(self, form):
        instance = form.save()
        # 커모의 작성자는 디폴트로 참여해야 하고, 작성자에게 참가 점수를 부여한다.
        author_active = ActiveUser.objects.filter(user=instance.author).latest()
        instance.participate_or_not(author_active)
        self.message = '{}님이 커모를  열었습니다. 아래 링크에서 확인해주세요!'.format(self.request.user.name)
        if self.request.FILES:
            if not 'save_cafephoto' in self.request.POST:
                # 사용자가 그냥 flag를 넣지 않았다면 그냥 모임사진으로 저장한다.
                for f in self.request.FILES.getlist('images'):
                    photo = MeetingPhoto(meeting=instance, image=f)
                    photo.save()
            else:
                # 사용자가 flag를 넣었으면 카페 자체의 사진으로 저장한다.
                for f in self.request.FILES.getlist('images'):
                    photo = CafePhoto(cafe_id=self.request.POST['cafe'], image=f)
                    photo.save()
        return super(CoffeeMeetingCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CoffeeMeetingCreateView, self).get_context_data(**kwargs)
        context['cafe'] = self.cafe
        return context


class CoffeeMeetingUpdateView(ValidAuthorRequiredMixin, CoffeeMeetingCreateUpdateMixin, UpdateView):
    def get_success_url(self, **kwargs):
        return reverse_lazy('meetings:coffee-meeting-detail', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        form_kwargs = super(CoffeeMeetingUpdateView, self).get_form_kwargs()
        form_kwargs['request'] = self.request
        form_kwargs['cafes'] = self.object.cafe
        # 수정할 때는 CoffeeMeetingForm에서 cafes 어트리뷰트를 수정할 수 있어야 한다
        form_kwargs['read_only'] = False
        return form_kwargs

    def form_valid(self, form):
        instance = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhoto(meeting=instance, image=f)
                photo.save()
        return super(CoffeeMeetingUpdateView, self).form_valid(form)


class CoffeeMeetingListView(LoginRequiredMixin, ListView):
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(CoffeeMeetingListView, self).get_context_data(*args, **kwargs)
        context['type'] = 'all'
        return context

    def get_queryset(self):
        queryset = CoffeeMeeting.objects \
            .select_related('author') \
            .select_related('cafe') \
            .prefetch_related('cafe__photos') \
            .prefetch_related('participants__user') \
            .prefetch_related('photos') \
            .all().order_by('-meeting_date')
        return queryset


class CoffeeMeetingUserListView(LoginRequiredMixin, ListView):
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(CoffeeMeetingUserListView, self).get_context_data(*args, **kwargs)
        context['type'] = 'user'
        return context

    def get_queryset(self):
        queryset = CoffeeMeeting.objects \
            .select_related('author') \
            .select_related('cafe') \
            .prefetch_related('cafe__photos') \
            .prefetch_related('participants__user') \
            .prefetch_related('photos') \
            .all().filter(author=self.request.user).order_by('-meeting_date')
        return queryset


class CoffeeMeetingDetailView(LoginRequiredMixin, FormMixin, DetailView):
    form_class = CommentForm
    queryset = CoffeeMeeting.objects \
        .prefetch_related('participants') \
        .prefetch_related('participants__user') \
        .select_related('cafe') \
        .prefetch_related('comments__author') \
        .select_related('author')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().is_past_due:
            return HttpResponseForbidden()
        return super(CoffeeMeetingDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CoffeeMeetingDetailView, self).get_context_data()
        context['user'] = self.request.user
        context['participated'] = True if ActiveUser.objects.filter(
            user=self.request.user).latest() in self.object.participants.all() else False
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context


# Participate View
@login_required()
def participate_meeting(request, pk):
    if request.method == 'POST':
        meeting = get_object_or_404(Meeting, pk=pk)
        if meeting.can_participate():
            # 참여가능인원이 다 차지 않은 경우 가장 최신의 활동회원 객체를 불러온다.
            active_user = ActiveUser.objects.filter(user=request.user)
            if active_user:
                active_user = active_user.latest()
                latest_os = OperationScheme.latest()
                # 이번 년도,학기와 활동회원의 년도, 학기가 다르면 참여할 수 없다.
                if not (active_user.active_year, active_user.active_semester) == \
                       (latest_os.current_year, latest_os.current_semester):
                    raise PermissionDenied('이번학기 활동회원만이 커모에 참가할 수 있습니다.')
                # 참여하거나 아니면 참여취소후 여부를 boolean flag로 반환한다.
                flag = meeting.participate_or_not(active_user)
                messages.success(request, "참여했습니다") if flag else messages.success(request, "참여 취소되었습니다.")
            return redirect(meeting.cast())
        else:
            messages.error(request, '참여 인원이 다 찼습니다.')
            return redirect(meeting.cast())


@login_required()
def delete_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    # 운영진이거나 글쓴이인 경우에만 삭제를 허용한다.
    if request.user == meeting.author or request.user.is_staff or request.user.is_superuser:
        if isinstance(meeting.cast(), CoffeeMeeting):
            # 현재 지운 meeting이 커모였다면 커모 리스트로 이동한다.
            meeting.delete()
            return redirect('meetings:coffee-meeting-list')
        else:
            # 공식모임이나 커피교육은 반드시 운영진이 지워야 한다.
            if not request.user.is_staff:
                raise PermissionDenied
            # 아니라면 공식모임 또는 커피교육이므로 해당 리스트로 이동한다.
            meeting.delete()
            return redirect('meetings:meetings-list')
    else:
        raise PermissionDenied
