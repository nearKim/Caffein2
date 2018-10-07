from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView, FormMixin)

from comments.forms import CommentForm
from core.mixins import FaceBookPostMixin, ValidAuthorRequiredMixin
from core.models import FeedPhoto, OperationScheme, Instagram
from meetings.models import CoffeeMeeting
from partners.forms import PartnerMeetingForm, CoffeeMeetingFeedForm
from partners.mixins import PartnerMeetingUpdateCreateMixin, CoffeeMeetingFeedUpdateCreateMixin
from partners.models import PartnerMeeting, CoffeeMeetingFeed
from .models import (
    PartnerMeeting,
    Partner
)


class FeedListView(LoginRequiredMixin, FormMixin, ListView):
    # TODO: Add infinite scroll feature
    form_class = CommentForm
    template_name = 'partners/feed_list.html'

    def get_context_data(self, **kwargs):
        context = super(FeedListView, self).get_context_data(**kwargs)
        context['comment_form'] = self.get_form()
        return context

    def get_queryset(self):
        latest_os = OperationScheme.latest()
        # 짝모와 커모 후기를 같이 보여준다.
        queryset = Instagram.objects \
            .prefetch_related('photos') \
            .select_related('author') \
            .select_related('partnermeeting__partner') \
            .select_related('coffeemeetingfeed') \
            .prefetch_related('comments__author') \
            .filter(created__gte=latest_os.semester_start) \
            .order_by('-created', '-modified')
        return queryset


class PartnerMeetingDeleteView(ValidAuthorRequiredMixin, DeleteView):
    model = PartnerMeeting
    success_url = reverse_lazy('partners:meeting-list')


class PartnerMeetingUpdateView(ValidAuthorRequiredMixin, PartnerMeetingUpdateCreateMixin, UpdateView):
    def form_valid(self, form):
        instance = form.save()
        FeedPhoto.objects.filter(instagram=instance).delete()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                feed_photo = FeedPhoto(instagram=instance, image=f)
                feed_photo.save()

        return super(PartnerMeetingUpdateView, self).form_valid(form)


class PartnerMeetingCreateView(LoginRequiredMixin, FaceBookPostMixin, PartnerMeetingUpdateCreateMixin, CreateView):
    def get(self, request, **kwargs):
        # 유저가 속한 최신의 짝지 객체를 가져온다.
        try:
            latest_partner = Partner.related_partner_user(request.user)
            current_os = OperationScheme.latest()
            # 짝지 객체가 있는경우 짝지의 년도-학기를 현재 최신의 운영정보의 년도-학기와 비교한다
            if latest_partner is None:
                raise Http404
                # 다른경우 신학기 시작 후 기존회원의 옛날 짝지 데이터를 가져온 것이므로 에러 메세지를 띄우고 index로 보낸다.
            elif not ((current_os.current_year == latest_partner.partner_year) and (
                    current_os.current_semester == latest_partner.partner_semester)):
                raise Http404
            else:
                return super(PartnerMeetingCreateView, self).get(self, request, **kwargs)
        except Http404:
            # 만일 짝지 객체가 없으면 신입회원이므로 에러 메세지를 띄우고 index로 보낸다.
            messages.error(request, '아직 짝지가 배정되지 않았습니다.')
            return redirect(reverse('core:index'))

    def form_valid(self, form):
        instance = form.save()
        self.message = '{}님이 짝모했어요!. 아래 링크에서 확인해주세요!'.format(self.request.user.name)
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                feed_photo = FeedPhoto(instagram=instance, image=f)
                feed_photo.save()

        return super(PartnerMeetingCreateView, self).form_valid(form)


class CoffeeMeetingFeedCreateView(LoginRequiredMixin, CoffeeMeetingFeedUpdateCreateMixin, CreateView):
    def dispatch(self, request, *args, **kwargs):
        coffee_meeting_pk = self.kwargs['pk']
        print(coffee_meeting_pk)
        if CoffeeMeeting.objects.filter(pk=coffee_meeting_pk).exists():
            messages.warning(request, '이미 선택하신 커모의 후기가 작성되어 있습니다. 여기서 확인해주세요!')
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(reverse('partners:meeting-list'))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['coffee_meeting'] = CoffeeMeeting.objects.get(pk=self.kwargs['pk'])
        return form_kwargs

    def form_valid(self, form):
        instance = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                feed_photo = FeedPhoto(instagram=instance, image=f)
                feed_photo.save()
        return super().form_valid(form)


class CoffeeMeetingFeedUpdateView(ValidAuthorRequiredMixin, CoffeeMeetingFeedUpdateCreateMixin, UpdateView):
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['coffee_meeting'] = self.get_object().coffee_meeting
        return form_kwargs

    def form_valid(self, form):
        instance = form.save()
        FeedPhoto.objects.filter(instagram=instance).delete()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                feed_photo = FeedPhoto(instagram=instance, image=f)
                feed_photo.save()
        return super().form_valid(form)


class CoffeeMeetingFeedDeleteView(ValidAuthorRequiredMixin, DeleteView):
    model = CoffeeMeetingFeed
    success_url = reverse_lazy('partners:meeting-list')


# Deprecated
class PartnerDetailView(DetailView):
    model = Partner
