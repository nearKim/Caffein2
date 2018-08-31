from django.forms import (
    ModelForm,
    forms,
    ClearableFileInput,
    DateTimeInput,
    HiddenInput)

from .models import (
    OfficialMeeting,
    CoffeeEducation,
    CoffeeMeeting)


class OfficialMeetingForm(ModelForm):
    class Meta:
        model = OfficialMeeting
        fields = ['title', 'content', 'category', 'location', 'meeting_date', 'max_participants', 'mapx', 'mapy']
        widgets = {'meeting_date': DateTimeInput(attrs={'id': 'inline_datetimepicker'})}

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OfficialMeetingForm, self).__init__(*args, **kwargs)
        self.fields['meeting_date'].input_formats = ["%Y-%m-%d %I:%M %p"]
        self.fields['mapx'].widget = HiddenInput()
        self.fields['mapy'].widget = HiddenInput()

    def save(self, commit=True):
        instance = super(OfficialMeetingForm, self).save(commit=False)
        instance.author = self.request.user
        instance.save()

        return instance


class CoffeeEducationForm(ModelForm):
    class Meta:
        model = CoffeeEducation
        fields = ['title', 'content', 'category', 'difficulty', 'location', 'meeting_date', 'max_participants', 'mapx', 'mapy']
        widgets = {'meeting_date': DateTimeInput(attrs={'id': 'inline_datetimepicker'})}

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CoffeeEducationForm, self).__init__(*args, **kwargs)
        self.fields['meeting_date'].input_formats = ["%Y-%m-%d %I:%M %p"]
        self.fields['mapx'].widget = HiddenInput()
        self.fields['mapy'].widget = HiddenInput()

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
        # kwargs에서 form을 만드는데 필요없는 view에서 넘겨준 부가정보를 먼저 빼낸다
        self.request = kwargs.pop('request', None)
        self.cafe = kwargs.pop('cafes')
        read_only = kwargs.pop('read_only')

        # form을 생성하고 필요한 처리를 한다
        super(CoffeeMeetingForm, self).__init__(*args, **kwargs)
        self.fields['cafe'].initial = self.cafe

        # UpdateView에서 넘어온 경우 cafe를 활성화한다
        if read_only:
            self.fields['cafe'].widget.attrs['readonly'] = True
        self.fields['meeting_date'].input_formats = ["%Y-%m-%d %I:%M %p"]

    def clean_cafe(self):
        # 카페의 경우 항상 url 인자로 넘어온 카페를 리턴해야 한다
        return self.cafe

    def save(self, commit=True):
        instance = super(CoffeeMeetingForm, self).save(commit=False)
        instance.author = self.request.user
        instance.cafe = self.cafe
        instance.save()
        return instance
