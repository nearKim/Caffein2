from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
from core.mixins import FaceBookPostMixin, StaffRequiredMixin
from meetings.mixins import OfficialMeetingCreateUpdateMixin, CoffeeEducationCreateUpdateMixin, \
    CoffeeMeetingCreateUpdateMixin
from .models import (
    OfficialMeeting,
    CoffeeEducation,
    CoffeeMeeting)
from core.models import Meeting, MeetingPhoto, OperationScheme


# 모든 모임을 한 화면에 보여주는 ListView
class EveryMeetingListView(LoginRequiredMixin, ListView):
    model = OfficialMeeting
    template_name = 'meetings/meeting_list.html'
    ordering = ['-created']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EveryMeetingListView, self).get_context_data(**kwargs)
        context['coffee_education_list'] = CoffeeEducation.objects.order_by('-created')
        context['coffee_meeting_list'] = CoffeeMeeting.objects.order_by('-created')
        return context


# CRUD for OfficialMeeting

class OfficialMeetingCreateView(StaffRequiredMixin, FaceBookPostMixin, OfficialMeetingCreateUpdateMixin, CreateView):
    def get_success_url(self, **kwargs):
        return reverse_lazy('meetings:official-detail', kwargs={'pk': self.object.id})

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
        .select_related('author')

    def get_context_data(self, **kwargs):
        context = super(OfficialMeetingDetailView, self).get_context_data()
        context['user'] = self.request.user
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context


class OfficialMeetingDeleteView(StaffRequiredMixin, DeleteView):
    model = OfficialMeeting
    success_url = reverse_lazy('meetings:meetings-list')


# CoffeeEducation
class CoffeeEducationCreateView(StaffRequiredMixin, FaceBookPostMixin, CoffeeEducationCreateUpdateMixin, CreateView):
    def get_success_url(self, **kwargs):
        return reverse_lazy('meetings:education-detail', kwargs={'pk': self.object.id})

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
        .select_related('author')

    def get_context_data(self, **kwargs):
        context = super(CoffeeEducationDetailView, self).get_context_data()
        context['user'] = self.request.user
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context


class CoffeeEducationDeleteView(StaffRequiredMixin, DeleteView):
    model = CoffeeEducation
    success_url = reverse_lazy('meetings:meetings-list')


# CoffeeMeeting
class CoffeeMeetingCreateView(LoginRequiredMixin, FaceBookPostMixin, CoffeeMeetingCreateUpdateMixin, CreateView):
    def get_success_url(self, **kwargs):
        return reverse_lazy('meetings:coffee-meeting-detail', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        form_kwargs = super(CoffeeMeetingCreateView, self).get_form_kwargs()
        form_kwargs['request'] = self.request
        form_kwargs['cafes'] = get_object_or_404(Cafe, pk=self.kwargs['pk'])
        form_kwargs['read_only'] = True
        return form_kwargs

    def form_valid(self, form):
        instance = form.save()
        # 커모의 작성자는 디폴트로 참여해야 한다.
        author_active = ActiveUser.objects.filter(user=instance.author).latest()
        instance.participants.add(author_active)
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
        context['cafe'] = get_object_or_404(Cafe, pk=self.kwargs['pk'])
        return context


class CoffeeMeetingUpdateView(LoginRequiredMixin, CoffeeMeetingCreateUpdateMixin, UpdateView):
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


class CoffeeMeetingDeleteView(LoginRequiredMixin, DeleteView):
    model = CoffeeMeeting
    success_url = reverse_lazy('meetings:meetings-list')


class CoffeeMeetingListView(LoginRequiredMixin, ListView):
    model = CoffeeMeeting


class CoffeeMeetingDetailView(LoginRequiredMixin, FormMixin, DetailView):
    form_class = CommentForm
    queryset = CoffeeMeeting.objects \
        .prefetch_related('participants') \
        .prefetch_related('participants__user') \
        .select_related('cafe') \
        .select_related('author')

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
    if request.user == meeting.author or request.user.is_staff:
        meeting.delete()
    return redirect("meetings:meetings-list")
