from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'photo_albums/album_create.html'

    # uploader 자동 생성
    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super(AlbumCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('photo_albums:album_edit', kwargs={'album_id': self.object.pk})


class AlbumListView(LoginRequiredMixin, ListView):
    model = Album


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album


class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo


class AlbumEditView(LoginRequiredMixin, View):

    def get(self, request, album_id):
        if self.request.user == Album.objects.get(pk=album_id).uploader or self.request.user.is_staff:
            photos_list = Photo.objects.filter(album_id=album_id)
        else:
            photos_list = Photo.objects.filter(album_id=album_id, uploader=self.request.user)
        return render(self.request, 'photo_albums/album_edit.html', {'photos': photos_list,
                                                                     'album_name': Album.objects.get(pk=album_id).name,
                                                                     'album_id': album_id,
                                                                     'uploader': Album.objects.get(pk=album_id).uploader})

    def post(self, request, album_id):
        form = PhotoFormCrop(self.request.POST, self.request.FILES)
        # for crop image upload
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = Album.objects.get(id=album_id)
            photo.uploader = self.request.user
            photo.save()
            photos_list = Photo.objects.filter(album_id=album_id)
            return render(self.request, 'photo_albums/album_edit.html',
                          {'photos': photos_list, 'album_id': album_id})
        # for many images upload.
        else:
            form = PhotoFormMultiFile(self.request.POST, self.request.FILES)
            photo = form.save(commit=False)
            photo.album = Album.objects.get(id=album_id)
            photo.uploader = self.request.user
            photo.save()
            # 페이지의 table에 바로 데이터를 붙이기위해 해당 데이터를 같이 전송.
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url, 'id': photo.id,
                    'absolute_url': photo.get_absolute_url(), 'thumb_url': photo.thumbnail.url}
            return JsonResponse(data)


@login_required
def clear_database(request, pk):
    for photo in Photo.objects.filter(album_id=pk):
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


# album edit에서 delete. album edit 페이지로 돌아감
@login_required
def delete_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    album_id = photo.album_id
    photo.file.delete()
    photo.delete()
    return redirect('photo_albums:album_edit', album_id=album_id)


# photo detail에서 delete. photo detail 페이지로 돌아감
@login_required
def delete_photo_to_album_detail(request, pk):
    photo = Photo.objects.get(pk=pk)
    album_id = photo.album_id
    photo.file.delete()
    photo.delete()
    return redirect('photo_albums:album_detail', pk=album_id)




