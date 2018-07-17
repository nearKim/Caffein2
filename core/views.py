from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)

from core.models import Comment


def index(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/index.html', context={'user': request.user})
    else:
        return render(request, 'index.html')


class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.author = self.request.user
        form.instagram.pk = self.kwargs.get('insta_pk')
        return super().form_valid(form)


class CommentDetailView(DetailView):
    model = Comment


class CommentListView(ListView):
    model = Comment
    ordering = ['-created', '-modified']


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['content']


class CommentDeleteView(DeleteView):
    model = Comment
