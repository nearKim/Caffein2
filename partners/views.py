from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)

from .forms import PartnerMeetingForm
from .models import (
    PartnerMeeting,
    Partners
)


class PartnerDetailView(DetailView):
    model = Partners


class PartnerMeetingListView(ListView):
    model = PartnerMeeting


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
    pass


class PartnerMeetingCreateView(PartnerMeetingUpdateCreateMixin, CreateView):
    pass
