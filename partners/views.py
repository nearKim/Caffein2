from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView, FormMixin)

from core.forms import CommentForm
from core.models import FeedPhotos
from .forms import PartnerMeetingForm
from .models import (
    PartnerMeeting,
    Partners
)


class PartnerDetailView(DetailView):
    model = Partners


class PartnerMeetingListView(FormMixin, ListView):
    # TODO: Add infinite scroll feature
    model = PartnerMeeting
    form_class = CommentForm
    ordering = ['-created', '-modified']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PartnerMeetingListView, self).get_context_data(**kwargs)
        context['comment_form'] = self.get_form()
        return context


class PartnerMeetingDeleteView(DeleteView):
    model = PartnerMeeting
    success_url = reverse_lazy('partners:meeting-list')


class PartnerMeetingUpdateCreateMixin:
    model = PartnerMeeting
    form_class = PartnerMeetingForm
    success_url = reverse_lazy('partners:meeting-list')

    class Meta:
        abstract = True

    def get_form_kwargs(self):
        form_kwargs = super(PartnerMeetingUpdateCreateMixin, self).get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs


class PartnerMeetingUpdateView(PartnerMeetingUpdateCreateMixin, UpdateView):
    def form_valid(self, form):
        instance = form.save()
        FeedPhotos.objects.filter(instagram=instance).delete()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                feed_photo = FeedPhotos(instagram=instance, image=f)
                feed_photo.save()

        return super(PartnerMeetingUpdateView, self).form_valid(form)


class PartnerMeetingCreateView(PartnerMeetingUpdateCreateMixin, CreateView):
    def form_valid(self, form):
        instance = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                feed_photo = FeedPhotos(instagram=instance, image=f)
                feed_photo.save()

        return super(PartnerMeetingCreateView, self).form_valid(form)
