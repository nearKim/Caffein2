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
        fields = ['content', 'num_coffee', 'num_eat']

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}), label='짝모 사진')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.participants = kwargs.pop('participants', None)
        super(PartnerMeetingForm, self).__init__(*args, **kwargs)
        self.fields['participants'] = MultipleChoiceField(label='참가자',
                                                          choices=[(participant.user.pk, participant.user.name) for participant in
                                                                   self.participants],
                                                          widget=CheckboxSelectMultiple)

    def save(self, commit=True):
        instance = super(PartnerMeetingForm, self).save(commit=False)
        instance.partner = Partner.related_partner_user(self.request.user)
        instance.author = self.request.user
        instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        latest_os = OperationScheme.latest()
        partner = Partner.related_partner_activeuser(ActiveUser.objects.get(user=self.request.user,
                                                                            active_year=latest_os.current_year,
                                                                            active_semester=latest_os.current_semester))
        participants = cleaned_data.get('participants')
        # 아무도 선택하지 않았을때
        if participants is None:
            raise forms.ValidationError('짝모에 참가한 사람을 선택해주세요.')
        # 위짝지가 없으면 에러 발생
        elif str(partner.up_partner.user.pk) not in participants:
            raise forms.ValidationError('짝모에는 위짝지가 반드시 포함되어야 합니다.')
        # 아래짝지가 없어도 에러 발생
        elif len(participants) == 1:
            raise forms.ValidationError('짝모에는 아래짝지가 반드시 포함되어야 합니다.')


class CoffeeMeetingFeedForm(ModelForm):
    class Meta:
        model = CoffeeMeetingFeed
        fields = ['content', 'coffee_meeting']

    images = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}), label='커모 후기 사진')

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.coffee_meeting = kwargs.pop('coffee_meeting', None)
        self.participants = kwargs.pop('participants', None)
        super(CoffeeMeetingFeedForm, self).__init__(*args, **kwargs)
        # 커모는 바꾸면 안되겠지
        self.fields['coffee_meeting'].initial = self.coffee_meeting
        self.fields['coffee_meeting'].widget.attrs['readonly'] = True
        self.fields['participants'] = MultipleChoiceField(label='참가자',
                                                          choices=[(participant.pk, participant.name) for participant in self.participants],
                                                          widget=CheckboxSelectMultiple)

    def clean_coffee_meeting(self):
        # 항상 넘어온 커모를 리턴한다
        return self.coffee_meeting

    def save(self, commit=True):
        instance = super(CoffeeMeetingFeedForm, self).save(commit=False)
        instance.author = self.author
        instance.save()
        return instance
