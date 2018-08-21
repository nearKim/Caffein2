from django.urls import reverse_lazy

from meetings.forms import OfficialMeetingForm, CoffeeEducationForm, CoffeeMeetingForm
from meetings.models import OfficialMeeting, CoffeeEducation, CoffeeMeeting


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


class CoffeeMeetingCreateUpdateMixin:
    model = CoffeeMeeting
    form_class = CoffeeMeetingForm

    class Meta:
        abstract = True

    def get_success_url(self):
        return reverse_lazy('meetings:coffee-meeting-detail', args=[self.object.pk])


class AddContextDetailViewMixin:
    def get_context_data(self, **kwargs):
        context = super(AddContextDetailViewMixin, self).get_context_data()
        context['user'] = self.request.user
        context['comments'] = self.object.comments
        context['comment_form'] = self.get_form()
        return context

    class Meta:
        abstract = True