from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)

from core.models import Comment, Instagram
from meetings.models import Meeting


# Home view for anonymous users

def index(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/index.html', context={'user': request.user})
    else:
        return render(request, 'index.html')


# Comment Views

class InstagramCommentCreateView(CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.instance.instagram = Instagram.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        return HttpResponseRedirect(self.request.POST.get('next', '/'))


class MeetingCommentCreateView(CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.instance.meeting = Meeting.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        return HttpResponseRedirect(self.request.POST.get('next', '/'))


class CommentUpdateView(UpdateView):
    model = Comment
    template_name_suffix = '_update_form'
    fields = ['content']

    def get_success_url(self):
        return Comment.objects.get(pk=self.kwargs['pk']).get_absolute_url()

    # def get_success_url(self):
    #     from_path = self.kwargs['from']
    #     if from_path == 'partner':
    #         return reverse_lazy('partners:meeting-list')
    #     elif from_path == 'official':
    #         return reverse_lazy('meetings:official-detail')
    #     elif from_path == 'education':
    #         return reverse_lazy('meetings:education-detail')


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        # 이전 페이지로 이동
        to = self.request.POST.get('next', '/')
        return to
