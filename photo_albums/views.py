import json

from django.db import transaction
from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView
from django.http import JsonResponse

from photo_albums.forms import PhotoUploadForm
from photo_albums.models import Album, Photo


class PhotoAlbumMainView(TemplateView):
    template_name = 'photo_albums/photo_album_main.html'


class AlbumListAjaxView(ListView):
    template_name = 'ajax/album_list.html'
    context_object_name = 'album_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Album.objects \
            .prefetch_related('photos') \
            .select_related('uploader') \
            .all()
        return queryset


class PhotoListAjaxView(ListView):
    template_name = 'ajax/photo_list.html'
    context_object_name = 'photos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Photo.objects \
            .select_related('uploader') \
            .select_related('album') \
            .prefetch_related('comments__author') \
            .all()
        return queryset


def album_create_ajax_view(request):
    if request.method == 'POST':
        # 모달에서 앨범명, 앨범 설명, 각 사진에 대한 PK와 설명이 넘어온다.
        album_name = request.POST.get('album-name')
        album_desc = request.POST.get('album-description')
        photo_descs = json.loads(request.POST.get('photo-descriptions'))

        try:
            # 앨범을 제일 먼저 생성한다.
            album = Album.objects.create(name=album_name, description=album_desc, uploader=request.user)
            # 각 사진객체의 앨범을 위에서 생성한 앨범과 연결하고 설명을 업데이트 한다.
            with transaction.atomic():
                for pk, desc in photo_descs.items():
                    Photo.objects.filter(pk=pk).update(description=desc, album=album)
        except:
            response = JsonResponse({'success': False})
            response.status_code = 500
            return response
        return JsonResponse({'success': True})


def photo_create_ajax_view(request):
    if request.method == 'POST':
        # 사진을 업로드하면 AJAX를 이용하여 사진 인스턴스를 생성한다.
        # 나머지 필드는 앨범을 생성할 때 채워준다.
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.album = None
            photo.save()
            context = {'is_valid': True, 'thumb_url': photo.thumbnail.url, 'pk': photo.pk}
        else:
            context = {'is_valid': False}
        return render(request, 'ajax/photo_create_view.html', context)


class PhotoCreateAjaxView(CreateView):
    # 일단 사진을 업로드하면 AJAX를 이용해 사진 인스턴스를 생성한다.
    # 나머지는 앨범을 생성할 때 채워줄 것이므로 빈칸으로 놔둔다.
    model = Photo
    form_class = PhotoUploadForm
    template_name = 'ajax/photo_create_view.html'

    def form_valid(self, form):
        instance = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('photo'):
                photo = Photo(photo=f, uploader=self.request.user)
                photo.save()

            data = {'is_valid': True, 'photo_pk': photo.pk, 'name': photo.photo.name, 'url': photo.photo.url,
                    'thumb_url': photo.thumbnail.url}

        else:
            data = {'is_valid': False}

        return JsonResponse(data)
