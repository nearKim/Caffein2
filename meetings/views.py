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
from cafes.models import Cafe
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
    def form_valid(self, form):
        instance = form.save()
        self.message = '{}님이 공식모임을 생성하였습니다. 아래 링크에서 확인해주세요!'.format(self.request.user.name)
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhoto(meeting=instance, image=f)
                photo.save()
        return super(OfficialMeetingCreateView, self).form_valid(form)


class OfficialMeetingUpdateView(StaffRequiredMixin, OfficialMeetingCreateUpdateMixin, UpdateView):

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
    model = OfficialMeeting
    form_class = CommentForm

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
    def form_valid(self, form):
        instance = form.save()
        self.message = '{}님이 커피교육을 열었습니다. 아래 링크에서 확인해주세요!'.format(self.request.user.name)
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhoto(meeting=instance, image=f)
                photo.save()
        return super(CoffeeEducationCreateView, self).form_valid(form)


class CoffeeEducationUpdateView(StaffRequiredMixin, CoffeeEducationCreateUpdateMixin, UpdateView):
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
    model = CoffeeEducation
    form_class = CommentForm

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
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhoto(meeting=instance, image=f)
                photo.save()
        return super(CoffeeMeetingCreateView, self).form_valid(form)


class CoffeeMeetingUpdateView(LoginRequiredMixin, CoffeeEducationCreateUpdateMixin, UpdateView):
    template_name_suffix = '_update_form'

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
    model = CoffeeMeeting
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(CoffeeMeetingDetailView, self).get_context_data()
        context['user'] = self.request.user
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context


# Participate View
@login_required()
def participate_meeting(request, pk):
    if request.method == 'POST':
        meeting = get_object_or_404(Meeting, pk=pk)

        if meeting.can_participate():
            # 참여가능인원이 다 차지 않은 경우
            active_user = get_object_or_404(ActiveUser, user=request.user)
            # 참여하거나 아니면 참여취소후 여부를 boolean flag로 반환한다.
            flag = meeting.participate_or_not(active_user)
            messages.info(request, "참여했습니다") if flag else messages.info(request, "참여 취소되었습니다.")
            return redirect(meeting.cast())
        else:
            messages.error(request, '참여 인원이 다 찼습니다.')
            return redirect(meeting.cast())
