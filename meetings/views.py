from django.contrib import messages
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
    FormMixin)

from accounts.models import ActiveUser
from cafe.models import Cafe
from comments.forms import CommentForm
from meetings.mixins import OfficialMeetingCreateUpdateMixin, CoffeeEducationCreateUpdateMixin, \
    CoffeeMeetingCreateUpdateMixin
from .models import (
    OfficialMeeting,
    CoffeeEducation,
    CoffeeMeeting)
from core.models import Meeting, MeetingPhotos


# 모든 모임을 한 화면에 보여주는 ListView
class EveryMeetingListView(ListView):
    model = OfficialMeeting
    template_name = 'meetings/meeting_list.html'
    ordering = ['-created']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EveryMeetingListView, self).get_context_data(**kwargs)
        context['coffee_education_list'] = CoffeeEducation.objects.order_by('-created')
        context['coffee_meeting_list'] = CoffeeMeeting.objects.order_by('-created')
        return context


# CRUD for OfficialMeeting

class OfficialMeetingCreateView(OfficialMeetingCreateUpdateMixin, CreateView):
    def form_valid(self, form):
        instance = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhotos(meeting=instance, image=f)
                photo.save()
        return super(OfficialMeetingCreateView, self).form_valid(form)


class OfficialMeetingUpdateView(OfficialMeetingCreateUpdateMixin, UpdateView):
    def form_valid(self, form):
        instance = form.save()
        MeetingPhotos.objects.filter(meeting=instance).delete()

        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhotos(meeting=instance, image=f)
                photo.save()

        return super(OfficialMeetingUpdateView, self).form_valid(form)


class OfficialMeetingListView(ListView):
    model = OfficialMeeting


class OfficialMeetingDetailView(FormMixin, DetailView):
    model = OfficialMeeting
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(OfficialMeetingDetailView, self).get_context_data()
        context['user'] = self.request.user
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context


class OfficialMeetingDeleteView(DeleteView):
    model = OfficialMeeting
    success_url = reverse_lazy('meetings:meetings-list')


# CoffeeEducation
class CoffeeEducationCreateView(CoffeeEducationCreateUpdateMixin, CreateView):
    def form_valid(self, form):
        instance = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhotos(meeting=instance, image=f)
                photo.save()
        return super(CoffeeEducationCreateView, self).form_valid(form)


class CoffeeEducationUpdateView(CoffeeEducationCreateUpdateMixin, UpdateView):
    def form_valid(self, form):
        instance = form.save()
        MeetingPhotos.objects.filter(meeting=instance).delete()

        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhotos(meeting=instance, image=f)
                photo.save()

        return super(CoffeeEducationUpdateView, self).form_valid(form)


class CoffeeEducationListView(ListView):
    model = CoffeeEducation


class CoffeeEducationDetailView(FormMixin, DetailView):
    model = CoffeeEducation
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(CoffeeEducationDetailView, self).get_context_data()
        context['user'] = self.request.user
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context


class CoffeeEducationDeleteView(DeleteView):
    model = CoffeeEducation
    success_url = reverse_lazy('meetings:meetings-list')


# CoffeeMeeting
class CoffeeMeetingCreateView(CoffeeMeetingCreateUpdateMixin, CreateView):
    def get_form_kwargs(self):
        form_kwargs = super(CoffeeMeetingCreateView, self).get_form_kwargs()
        form_kwargs['request'] = self.request
        form_kwargs['cafe'] = get_object_or_404(Cafe, pk=self.kwargs['pk'])
        form_kwargs['read_only'] = True
        return form_kwargs

    def form_valid(self, form):
        instance = form.save()
        # 커모의 작성자는 디폴트로 참여해야 한다.
        author_active = ActiveUser.objects.filter(user=instance.author).latest()
        instance.participants.add(author_active)
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhotos(meeting=instance, image=f)
                photo.save()
        return super(CoffeeMeetingCreateView, self).form_valid(form)


class CoffeeMeetingUpdateView(CoffeeEducationCreateUpdateMixin, UpdateView):
    template_name_suffix = '_update_form'

    def get_form_kwargs(self):
        form_kwargs = super(CoffeeMeetingUpdateView, self).get_form_kwargs()
        form_kwargs['request'] = self.request
        form_kwargs['cafe'] = self.object.cafe
        # 수정할 때는 CoffeeMeetingForm에서 cafe 어트리뷰트를 수정할 수 있어야 한다
        form_kwargs['read_only'] = False
        return form_kwargs

    def form_valid(self, form):
        instance = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                photo = MeetingPhotos(meeting=instance, image=f)
                photo.save()
        return super(CoffeeMeetingUpdateView, self).form_valid(form)


class CoffeeMeetingDeleteView(DeleteView):
    model = CoffeeMeeting
    success_url = reverse_lazy('meetings:meetings-list')


class CoffeeMeetingListView(ListView):
    model = CoffeeMeeting


class CoffeeMeetingDetailView(FormMixin, DetailView):
    model = CoffeeMeeting
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(CoffeeMeetingDetailView, self).get_context_data()
        context['user'] = self.request.user
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context


# Participate View
def participate_meeting(request, pk):
    # TODO: 참여자를 스캔하여 짝지가 있으면 자동으로 점수 상향
    if request.method == 'POST':
        meeting = get_object_or_404(Meeting, pk=pk)
        if meeting.can_participate():
            active_user = get_object_or_404(ActiveUser, user=request.user)
            if active_user in meeting.participants.all():
                messages.info(request, '취소 되었습니다.')
                meeting.participants.remove(active_user)
            else:
                messages.info(request, '참여 했습니다.')
                meeting.participate_meeting(active_user)
            return redirect(meeting.cast())
        else:
            messages.error(request, '참여 인원이 다 찼습니다.')
            return redirect(meeting.cast())
