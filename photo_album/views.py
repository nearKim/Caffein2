from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm


from django.http import JsonResponse
from django.views import View
import time


class BasicUploadView(View):
    def get(self, request, album_id):
        photos_list = Photo.objects.filter(album_id=album_id)
        return render(self.request, 'photo_album/basic_upload/index.html', {'photos': photos_list})

    def post(self, request, album_id):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            #photo = form.save()
            photo = form.save(commit=False)
            photo.album = Album.objects.get(id=album_id)
            print(album_id)
            print(Album.objects.get(id=album_id))
            photo.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photo_album/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            print('bar')
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class DragAndDropUploadView(View):

    def get(self, request, album_id):
        photos_list = Photo.objects.filter(album_id=album_id)
        return render(self.request, 'photo_album/drag_and_drop_upload/index.html', {'photos': photos_list, 'album_id': album_id})

    def post(self, request, album_id):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            #photo = form.save()
            photo = form.save(commit=False)
            photo.album = Album.objects.get(id=album_id)
            print(album_id)
            print(Album.objects.get(id=album_id))
            photo.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


'''
def photo_list(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'photo_album/photo_list.html', {'form': form, 'photos': photos})
'''

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

