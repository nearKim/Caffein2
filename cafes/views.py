from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)

from cafes.forms import CafeCreateUpdateForm
from cafes.models import Cafe, CafePhoto

# deprecated
from meetings.models import CoffeeMeeting


class CafeListView(LoginRequiredMixin, ListView):
    context_object_name = 'cafes'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET['sort'] == 'popularity':
            queryset = Cafe.objects.prefetch_related('photos') \
                .select_related('last_modifier') \
                .select_related('uploader') \
                .prefetch_related('coffeemeeting_set') \
                .annotate(num_meetings=Count('coffeemeeting')) \
                .order_by('-num_meetings')
        elif self.request.GET['sort'] == 'recent':
            queryset = Cafe.objects.prefetch_related('photos') \
                .select_related('last_modifier') \
                .select_related('uploader') \
                .all() \
                .order_by('-created')
        elif self.request.GET['sort'] == 'photo':
            queryset = Cafe.objects.prefetch_related('photos') \
                .select_related('last_modifier') \
                .select_related('uploader') \
                .annotate(num_photo=Count('photos')) \
                .order_by('-num_photo')
        else:
            # Random
            queryset = Cafe.objects.prefetch_related('photos') \
                .select_related('last_modifier') \
                .select_related('uploader') \
                .all().order_by('?')
        return queryset


class CafeDetailView(LoginRequiredMixin, DetailView):
    model = Cafe
    template_name = 'cafes/cafe_detail.html'
    context_object_name = 'cafe'


class CafeUpdateView(LoginRequiredMixin, UpdateView):
    model = Cafe
    form_class = CafeCreateUpdateForm
    template_name = 'cafes/cafe_update.html'

    def form_valid(self, form):
        form.instance.last_modifier = self.request.user
        instance = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                cafe_photo = CafePhoto(cafe=instance, image=f)
                cafe_photo.save()
        return super(CafeUpdateView, self).form_valid(form)


class CafeCreateView(LoginRequiredMixin, CreateView):
    model = Cafe
    form_class = CafeCreateUpdateForm
    template_name = 'cafes/cafe_create.html'

    # 카페 최초 등록자 자동 생성
    def form_valid(self, form):
        form.instance.uploader = self.request.user
        instance = form.save()
        # 카페 사진이 같이 넘어왔다면 함께 저장하자
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                cafe_photo = CafePhoto(cafe=instance, image=f)
                cafe_photo.save()
        return super(CafeCreateView, self).form_valid(form)


class CafeSearchView(LoginRequiredMixin, ListView):
    """
    현재 카페인의 postgre 데이터베이스를 검색하여 카페 검색 결과를 반환한다.
    입력 키워드를 공백 기준으로 split하여 카페의 이름에 키워드가 포함된 결과들을 or하여 반환한다.
    """
    model = Cafe
    paginate_by = 20
    template_name = 'cafes/cafe_search.html'

    def get_queryset(self):
        keywords = self.request.GET.get('search-term', None)
        if keywords:
            qs = Cafe.objects.all()
            for keyword in keywords.split():
                qs = qs.filter(name__icontains=keyword)
        else:
            qs = Cafe.objects.none()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(CafeSearchView, self).get_context_data(*args, **kwargs)
        if Cafe.objects.all().count() > 2:
            # 현재 카페들중 3개를 랜덤하게 뽑아온다. 카페들은 많아봤자 몇십~몇백개일 것이므로 퍼포먼스 이슈는 없다.
            context['random_cafes'] = Cafe.objects \
                                          .select_related('uploader') \
                                          .select_related('last_modifier') \
                                          .prefetch_related('photos') \
                                          .order_by('?')[:3]
        return context
