from django.urls import reverse_lazy

from meetings.models import CoffeeMeeting
from partners.forms import CoffeeMeetingFeedForm, PartnerMeetingForm
from partners.models import CoffeeMeetingFeed, PartnerMeeting


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


class CoffeeMeetingFeedUpdateCreateMixin:
    model = CoffeeMeetingFeed
    form_class = CoffeeMeetingFeedForm
    success_url = reverse_lazy('partners:meeting-list')

    class Meta:
        abstract = True

    def get_form_kwargs(self):
        form_kwargs = super(CoffeeMeetingFeedUpdateCreateMixin, self).get_form_kwargs()
        form_kwargs['author'] = self.request.user
        return form_kwargs
