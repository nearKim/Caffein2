from django.forms import (
    ModelForm,
    forms,
    ClearableFileInput)

from .models import (
    OfficialMeeting,
    CoffeeEducation,
    CoffeeMeeting)


class OfficialMeetingForm(ModelForm):
    class Meta:
        model = OfficialMeeting
        fields = ['title', 'content', 'category', 'location', 'meeting_date', 'max_participants']

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}),
                             required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OfficialMeetingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(OfficialMeetingForm, self).save(commit=False)
        instance.author = self.request.user
        instance.save()

        return instance


class CoffeeEducationForm(ModelForm):
    class Meta:
        model = CoffeeEducation
        fields = ['title', 'content', 'category', 'difficulty', 'location', 'meeting_date', 'max_participants']

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CoffeeEducationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CoffeeEducationForm, self).save(commit=False)
        instance.author = self.request.user
        instance.save()

        return instance
