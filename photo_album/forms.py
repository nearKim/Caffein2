from PIL import Image

from django import forms
from django.core.files import File

from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('name', 'description')


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )
    '''
    def save(self, **kwargs):
        photo = super().save(commit=False)
        print(kwargs.get('album_id'))
        photo.album = Album.objects.get(id=kwargs.get('album_id'))
        photo.save()
        return photo'''


class PhotoForm2(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self, **kwargs):
        photo = super(PhotoForm2, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))

        cropped_image.save(photo.file.path)
        return photo
