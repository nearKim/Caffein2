from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm, PhotoForm2
from django.http import JsonResponse
from django.views import View


class PhotoEditView(View):

    def get(self, request, album_id):
        photos_list = Photo.objects.filter(album_id=album_id)
        return render(self.request, 'photo_album/drag_and_drop_upload/index.html', {'photos': photos_list, 'album_id': album_id})

    def post(self, request, album_id):
        form = PhotoForm2(self.request.POST, self.request.FILES)
        # for crop image
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = Album.objects.get(id=album_id)
            photo.save()
            photos_list = Photo.objects.filter(album_id=album_id)
            return render(self.request, 'photo_album/drag_and_drop_upload/index.html',
                          {'photos': photos_list, 'album_id': album_id})
        # for many images
        else:
            form = PhotoForm(self.request.POST, self.request.FILES)
            photo = form.save(commit=False)
            photo.album = Album.objects.get(id=album_id)
            photo.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            return JsonResponse(data)
        #return redirect('photo_album:drag_and_drop_upload', album_id=album_id)


def clear_database(request, pk):
    for photo in Photo.objects.filter(album_id=pk):
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


def delete_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    album_id = photo.album_id
    photo.file.delete()
    photo.delete()
    return redirect('photo_album:drag_and_drop_upload', album_id=album_id)
    #return redirect(request.POST.get('next'))
    #return reverse('photo_album:drag_and_drop_upload', kwargs={'album_id': album_id})


def photo_crop(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        form = PhotoForm2(request.POST, request.FILES)
        print(request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'photo_album/photo_crop.html', {'form': form, 'photos': photos})


class AlbumCreateView(CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'photo_album/album_create.html'

    # uploader 자동 생성
    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super(AlbumCreateView, self).form_valid(form)

    def get_success_url(self):
        #return render(self.request, 'photo_album/drag_and_drop_upload/index.html', {'album_id': self.object.pk})
        return reverse('photo_album:drag_and_drop_upload', kwargs={'album_id': self.object.pk})


class AlbumLV(ListView):
    model = Album


class AlbumDV(DetailView):
    model = Album


class PhotoDV(DetailView):
    model = Photo

