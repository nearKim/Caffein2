from PIL import Image
from django import forms
from .models import Album, Photo
from django.core.files.storage import default_storage as storage


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('name', 'description')


class PhotoFormMultiFile(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )


class PhotoFormCrop(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'
            })
        }

    def save(self, **kwargs):
        photo = super(PhotoFormCrop, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        fh = storage.open(photo.file.name, 'w')
        cropped_image.save(fh, 'PNG')
        fh.close()

        return photo

