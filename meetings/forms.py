from django.conf import settings
from django.forms import (
    ModelForm,
    forms,
    ClearableFileInput,
    DateTimeInput,
    HiddenInput)
from django.shortcuts import get_object_or_404

from cafe.models import Cafe
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


class CoffeeMeetingForm(ModelForm):
    class Meta:
        model = CoffeeMeeting
        fields = ['title', 'content', 'cafe', 'meeting_date', 'max_participants']
        widgets = {'meeting_date': DateTimeInput(attrs={'id': 'inline_datetimepicker'})}

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.cafe = kwargs.pop('cafe')
        super(CoffeeMeetingForm, self).__init__(*args, **kwargs)
        # self.target_cafe = get_object_or_404(Cafe, pk=cafe_pk)
        self.fields['cafe'].initial = self.cafe
        self.fields['cafe'].widget.attrs['readonly'] = True
        self.fields['meeting_date'].input_formats = ["%Y-%m-%d %I:%M %p"]

    def clean_cafe(self):
        # 카페의 경우 항상 url 인자로 넘어온 카페를 리턴해야 한다
        return self.cafe

    def save(self, commit=True):
        instance = super(CoffeeMeetingForm, self).save(commit=False)
        instance.author = self.request.user
        instance.save()
        return instance
