import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, UpdateView
from django.http import JsonResponse, HttpResponseRedirect

from core.mixins import ValidAuthorRequiredMixin
from photo_albums.forms import PhotoUploadForm
from photo_albums.models import Album, Photo


class PhotoAlbumMainView(LoginRequiredMixin, TemplateView):
    template_name = 'photo_albums/photo_album_main.html'


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album

    def get_queryset(self):
        queryset = self.model.objects \
            .prefetch_related('photos') \
            .select_related('author') \
            .filter(pk=self.kwargs['pk'])
        return queryset


class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo

    def get_queryset(self):
        # 사진의 경우 앨범이 존재할 수도 없을수도 있다.
        queryset = self.model.objects \
            .select_related('author') \
            .select_related('album') \
            .select_related('album__author') \
            .filter(pk=self.kwargs['pk'])
        return queryset


# AJAX class based view
class AlbumListAjaxView(LoginRequiredMixin, ListView):
    template_name = 'ajax/album_list.html'
    context_object_name = 'album_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = Album.objects \
            .prefetch_related('photos') \
            .select_related('author') \
            .all()
        return queryset


class PhotoListAjaxView(LoginRequiredMixin, ListView):
    template_name = 'ajax/photo_list.html'
    context_object_name = 'photo_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = Photo.objects \
            .select_related('author') \
            .select_related('album') \
            .prefetch_related('comments__author') \
            .all()
        return queryset


# AJAX function based view
@login_required
def album_create_ajax_view(request):
    if request.method == 'POST':
        # 모달에서 앨범명, 앨범 설명, 각 사진에 대한 PK와 설명이 넘어온다.
        album_name = request.POST.get('album-name')
        album_desc = request.POST.get('album-description')
        photo_descs = json.loads(request.POST.get('photo-descriptions'))

        try:
            # 앨범을 제일 먼저 생성한다.
            album = Album.objects.create(name=album_name, description=album_desc, author=request.user)
            # 각 사진객체의 앨범을 위에서 생성한 앨범과 연결하고 설명을 업데이트 한다.
            with transaction.atomic():
                for pk, desc in photo_descs.items():
                    Photo.objects.filter(pk=pk).update(description=desc, album=album)
        except:
            response = JsonResponse({'success': False})
            response.status_code = 500
            return response
        return JsonResponse({'success': True})


@login_required
def photo_description_update_ajax_view(request):
    # 앨범 detail에서 사진추가를 했을 때 게시버튼을 누르면 호출되는 뷰.
    # Photo 객체들에는 이미 Album정보가 들어있는 상태이다.
    if request.method == 'POST':
        # REST에서는 PUT이겠지...
        try:
            photo_descs = json.loads(request.POST.get('photo-descriptions'))
            with transaction.atomic():
                for pk, desc in photo_descs.items():
                    Photo.objects.filter(pk=pk).update(description=desc)
        except:
            response = JsonResponse({'success': False})
            response.status_code = 500
            return response
        return JsonResponse({'success': True})


@login_required
def photo_create_ajax_view(request):
    if request.method == 'POST':
        # 사진을 업로드하면 AJAX를 이용하여 사진 인스턴스를 생성한다.
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.author = request.user
            if 'album' not in request.POST:
                # 앨범 메인에서 사진첩 추가로 들어왔다면 사진첩이 없으므로 None으로 먼저 세팅해준다
                photo.album = None
            else:
                # 만일 앨범상세 페이지에서 사진추가 버튼으로 들어왔다면 해당 앨범을 사진들에 넣어준다
                photo.album = Album.objects.get(pk=request.POST['album'])
            photo.save()
            context = {'is_valid': True, 'thumb_url': photo.thumbnail.url, 'pk': photo.pk}
        else:
            context = {'is_valid': False}
        return render(request, 'ajax/photo_create_view.html', context)


# Delete View
class AlbumDeleteView(ValidAuthorRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('photo_albums:photo-album-main')


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    # 단일 사진 객체를 삭제하는 view
    model = Photo

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # 사진의 업로더가 작성자이거나 운영진인 경우에만 삭제를 허용한다.
        if not (self.object.author == self.request.user or self.request.user.is_staff):
            raise PermissionDenied
        success_url = self.object.album.get_absolute_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class PhotoBatchDeleteView(LoginRequiredMixin, DeleteView):
    # 사진업로드 모달을 저장없이 닫았을 때 호출되어 앨범이 지정되지 않은 모든 사진 객체를 삭제한다.
    model = Photo

    def delete(self, request, *args, **kwargs):
        try:
            delete_targets_pks = request.POST.getlist('dangling-photos-pks[]')
            Photo.objects.filter(id__in=delete_targets_pks).all().delete()
            return JsonResponse({'success': True})
        except:
            response = JsonResponse({'success': False})
            response.status_code = 500
            return response


# Update View

class AlbumUpdateView(ValidAuthorRequiredMixin, UpdateView):
    model = Album
    fields = ('name', 'description')


class PhotoUpdateView(ValidAuthorRequiredMixin, UpdateView):
    model = Photo
    fields = ('description', 'photo')

    def get_success_url(self):
        album = self.get_object().album
        return reverse_lazy('photo_albums:album-detail', args=(album.pk,))
