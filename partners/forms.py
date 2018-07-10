from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from multiupload.fields import MultiImageField

from core.models import FeedPhotos
from .models import (
    PartnerMeeting,
    Partners
)


class ValidatedMultiImageField(MultiImageField):
    # https://github.com/Chive/django-multiupload/issues/23
    def run_validators(self, value):
        value = value or []

        for item in value:
            super().run_validators(item)


class PartnerMeetingForm(ModelForm):
    class Meta:
        model = PartnerMeeting
        fields = ['content', 'num_coffee', 'num_eat']

    images = ValidatedMultiImageField(min_num=0, max_num=10, help_text=_('10장까지 선택'), max_file_size=1024 * 1024 * 5)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PartnerMeetingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(PartnerMeetingForm, self).save(commit=False)
        instance.partner = Partners.related_partner(self.request.user)
        instance.author = self.request.user
        instance.save()

        for image in self.cleaned_data['images']:
            FeedPhotos.objects.create(image=image, instagram=instance)

        return instance
