from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .forms import *
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


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
