from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import (
    CreateView,
)

from .forms import PartnerMeetingForm
from .models import (
    PartnerMeeting,
    Partners
)


class PartnerDetailView(DetailView):
    model = Partners


class PartnerMeetingListView(ListView):
    model = PartnerMeeting


class PartnerMeetingCreateView(CreateView):
    model = PartnerMeeting
    form_class = PartnerMeetingForm
    template_name = 'partners/test.html'
    success_url = reverse('partners:meeting-list')

    def get_form_kwargs(self):
        form_kwargs = super(PartnerMeetingCreateView, self).get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs
