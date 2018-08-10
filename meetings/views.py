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
from core.forms import CommentForm
from .forms import (
    OfficialMeetingForm,
    CoffeeEducationForm,
    )
from .models import (
    OfficialMeeting,
    CoffeeEducation,
    MeetingPhotos, Meeting, CoffeeMeeting)


# ListView for showing every meeting

class EveryMeetingListView(ListView):
    model = OfficialMeeting
    template_name = 'meetings/meeting_list.html'
    ordering = ['-created']

    def get_context_data(self, *, object_list=None, **kwargs):
        # TODO: Add CoffeeMeeting objects
        context = super(EveryMeetingListView, self).get_context_data(**kwargs)
        context['coffee_education_list'] = CoffeeEducation.objects.order_by('-created')
        return context


# Mixins

class OfficialMeetingCreateUpdateMixin:
    model = OfficialMeeting
    form_class = OfficialMeetingForm
    success_url = reverse_lazy('meetings:meetings-list')

    class Meta:
        abstract = True

    def get_form_kwargs(self):
        form_kwargs = super(OfficialMeetingCreateUpdateMixin, self).get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs


class CoffeeEducationCreateUpdateMixin:
    model = CoffeeEducation
    form_class = CoffeeEducationForm
    success_url = reverse_lazy('meetings:meetings-list')

    class Meta:
        abstract = True

    def get_form_kwargs(self):
        form_kwargs = super(CoffeeEducationCreateUpdateMixin, self).get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs


class AddContextDetailViewMixin:
    def get_context_data(self, **kwargs):
        context = super(AddContextDetailViewMixin, self).get_context_data()
        context['user'] = self.request.user
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context

    class Meta:
        abstract = True


# CRUD for OfficialMeeting class


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


class OfficialMeetingDetailView(FormMixin, AddContextDetailViewMixin, DetailView):
    model = OfficialMeeting
    form_class = CommentForm


class OfficialMeetingDeleteView(DeleteView):
    model = OfficialMeeting
    success_url = reverse_lazy('meetings:meetings-list')


# CRUD for CoffeeEducation class


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


class CoffeeEducationDetailView(FormMixin, AddContextDetailViewMixin, DetailView):
    model = CoffeeEducation
    form_class = CommentForm


class CoffeeEducationDeleteView(DeleteView):
    model = CoffeeEducation
    success_url = reverse_lazy('meetings:meetings-list')


# TODO: Add CRUD for CoffeeMeeting model
# CoffeeMeeting View
class CoffeeMeetingCreateView(CreateView):
    pass


class CoffeeMeetingDeleteView(DeleteView):
    pass


class CoffeeMeetingUpdateView(UpdateView):
    pass


class CoffeeMeetingListView(ListView):
    pass


class CoffeeMeetingDetailView(DetailView):
    pass


# Participate View
def participate_meeting(request, pk):
    if request.method == 'POST':
        meeting = get_object_or_404(Meeting, pk=pk)
        active_user = get_object_or_404(ActiveUser, user=request.user)
        if active_user in meeting.participants.all():
            messages.info(request, '취소 되었습니다.')
            meeting.participants.remove(active_user)
        else:
            messages.info(request, '참여 했습니다.')
            meeting.participate_meeting(active_user)
        return redirect(meeting.cast())
