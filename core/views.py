from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)

from core.models import Comment, Instagram


def index(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/index.html', context={'user': request.user})
    else:
        return render(request, 'index.html')


class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.instance.instagram = Instagram.objects.get(pk=self.kwargs.get('insta_id'))
        form.save()
        return HttpResponseRedirect(self.request.POST.get('next', '/'))


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
