from django.http import HttpResponseRedirect

# Create your views here.
from django.views.generic import CreateView, UpdateView, DeleteView

from comments.models import Comment
from core.models import Instagram, Meeting


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


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        # 이전 페이지로 이동
        to = self.request.POST.get('next', '/')
        return to
