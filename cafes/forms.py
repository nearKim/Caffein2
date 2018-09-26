from django.forms import ModelForm, ClearableFileInput, forms
from django.forms.widgets import HiddenInput, TimeInput

from cafes.models import Cafe


class CafeCreateUpdateForm(ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'address', 'description', 'phone', 'machine', 'grinder', 'price', 'from_time', 'to_time',
                  'closed_day', 'closed_holiday', 'link', 'road_address', 'mapx', 'mapy']
        widgets = {'from_time': TimeInput(attrs={'id':'inline_timepicker_1'}),
                   'to_time': TimeInput(attrs={'id':'inline_timepicker_2'})}

    images = forms.FileField(required=False, widget=ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        super(CafeCreateUpdateForm, self).__init__(*args, **kwargs)
        # Javascript에서 dynamic하게 업데이트 해야 한다
        self.fields['road_address'].widget = HiddenInput()
        self.fields['mapx'].widget = HiddenInput()
        self.fields['mapy'].widget = HiddenInput()
        self.fields['from_time'].input_formats = ["%I:%M %p"]
        self.fields['to_time'].input_formats = ["%I:%M %p"]
