from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
@login_required
def index(request):
    num_cafes = Cafe.objects.all().count()
    context = {
        'num_cafes': num_cafes,
    }
    return render(request, 'cafes/index.html', context=context)


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
