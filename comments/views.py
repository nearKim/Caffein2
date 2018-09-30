from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404, render_to_response, render
from django.views.generic import CreateView, UpdateView, DeleteView

from comments.models import Comment
from core.mixins import ValidAuthorRequiredMixin
from core.models import Instagram, Meeting


class CommentCreateAjaxView(LoginRequiredMixin, CreateView):
    # 댓글 내용과 분기점을 받아서 적절한 FK를 찾아 연결하고 댓글 목록을 AJAX로 업데이트한다.
    model = Comment
    fields = ['content']
    template_name = 'comments/comments_container.html'

    def form_valid(self, form):
        to = self.kwargs.get('to')
        form.save(commit=False)
        form.instance.author = self.request.user

        if to == 'instagram':
            instagram = get_object_or_404(Instagram, pk=self.kwargs.get('pk'))
            form.instance.instagram = instagram
            context = {'comments': Comment.objects.filter(instagram=instagram)}

        elif to == 'meeting':
            meeting = get_object_or_404(Meeting, pk=self.kwargs.get('pk'))
            form.instance.meeting = meeting
            context = {'comments': Comment.objects.filter(meeting=meeting)}
        form.save()
        return render(self.request, 'comments/comments_container.html', context)


class CommentUpdateView(ValidAuthorRequiredMixin, UpdateView):
    model = Comment
    template_name_suffix = '_update_form'
    fields = ['content']

    def get_success_url(self):
        return Comment.objects.get(pk=self.kwargs['pk']).get_absolute_url()


class CommentDeleteView(ValidAuthorRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        # 이전 페이지로 이동
        to = self.request.POST.get('next', '/')
        return to


# Deprecated
class InstagramCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.instance.instagram = Instagram.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        return HttpResponseRedirect(self.request.POST.get('next', '/'))


class MeetingCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.instance.meeting = Meeting.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        return HttpResponseRedirect(self.request.POST.get('next', '/'))
