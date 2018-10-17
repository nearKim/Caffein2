from django.forms import ModelForm, forms, ClearableFileInput, MultipleChoiceField, CheckboxSelectMultiple, ChoiceField
from core.models import OperationScheme
from accounts.models import ActiveUser
from meetings.models import CoffeeMeeting
from .models import (
    PartnerMeeting,
    Partner,
    CoffeeMeetingFeed)


class PartnerMeetingForm(ModelForm):
    class Meta:
        model = PartnerMeeting
        fields = ['content', 'num_coffee', 'num_eat', 'num_down_partner']

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}), label='짝모 사진')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PartnerMeetingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(PartnerMeetingForm, self).save(commit=False)
        instance.partner = Partner.related_partner_user(self.request.user)
        instance.author = self.request.user
        instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        latest_os = OperationScheme.latest()
        down_len = Partner.related_partner_activeuser(ActiveUser.objects.get(user=self.request.user,
                                                                             active_year=latest_os.current_year,
                                                                             active_semester=latest_os.current_semester)).down_partner_count()
        # 아래짝지 수를 초과하는 입력시 validation error 발생
        if cleaned_data.get('num_down_partner') > down_len:
            raise forms.ValidationError('아래짝지의 수 {}명을 초과해서 입력할 수 없습니다.'.format(down_len))



class CoffeeMeetingFeedForm(ModelForm):
    class Meta:
        model = CoffeeMeetingFeed
        fields = ['content', 'coffee_meeting']

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}), label='커모 후기 사진')
    #participants = MultipleChoiceField(label='참가자', choices=clean_participants, widget=CheckboxSelectMultiple)


    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.coffee_meeting = kwargs.pop('coffee_meeting', None)
        self.participants = kwargs.pop('participants', None)
        super(CoffeeMeetingFeedForm, self).__init__(*args, **kwargs)
        # 커모는 바꾸면 안되겠지
        self.fields['coffee_meeting'].initial = self.coffee_meeting
        self.fields['coffee_meeting'].widget.attrs['readonly'] = True
        #self.fields['participants'].initial = self.participants
        self.fields['participants'] = MultipleChoiceField(label='참가자',
                                                          choices=[(participant.pk, participant.name) for participant in self.participants],
                                                          widget=CheckboxSelectMultiple,
                                                          )

    def clean_coffee_meeting(self):
        # 항상 넘어온 커모를 리턴한다
        return self.coffee_meeting

    def save(self, commit=True):
        instance = super(CoffeeMeetingFeedForm, self).save(commit=False)
        instance.author = self.author
        instance.save()
        return instance
