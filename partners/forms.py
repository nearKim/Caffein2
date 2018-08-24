from django.forms import ModelForm, forms, ClearableFileInput

from .models import (
    PartnerMeeting,
    Partners
)


class PartnerMeetingForm(ModelForm):
    class Meta:
        model = PartnerMeeting
        fields = ['content', 'num_coffee', 'num_eat']

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PartnerMeetingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(PartnerMeetingForm, self).save(commit=False)
        instance.partner = Partners.related_partner_user(self.request.user)
        instance.author = self.request.user
        instance.save()

        return instance
