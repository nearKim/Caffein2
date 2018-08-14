from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
)

from django.db.models import Q
from cafe.forms import CafeCreateUpdateForm
from cafe.models import Cafe


@login_required
def index(request):
    num_cafes = Cafe.objects.all().count()
    context = {
        'num_cafes': num_cafes,
    }
    return render(request, 'cafe/index.html', context=context)


class CafeListView(ListView, LoginRequiredMixin):
    model = Cafe
    template_name = 'cafe/cafe_list.html'


class CafeDetailView(DetailView, LoginRequiredMixin):
    model = Cafe
    template_name = 'cafe/cafe_detail.html'


class CafeDeleteView(DeleteView, LoginRequiredMixin):
    model = Cafe
    template_name = 'cafe/cafe_delete.html'


class CafeUpdateView(UpdateView, LoginRequiredMixin):
    model = Cafe
    form_class = CafeCreateUpdateForm
    template_name = 'cafe/cafe_update.html'


class CafeCreateView(CreateView, LoginRequiredMixin):
    model = Cafe
    form_class = CafeCreateUpdateForm
    template_name = 'cafe/cafe_create.html'

    # uploader 자동 생성
    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super(CafeCreateView, self).form_valid(form)


class CafeSearchView(ListView):
    """
    현재 카페인의 postgre 데이터베이스를 검색하여 카페 검색 결과를 반환합니다.
    입력 키워드를 공백 기준으로 split하여 카페의 이름에 키워드가 포함된 결과들을 or하여 반환합니다.
    """
    model = Cafe
    paginate_by = 20
    template_name = 'cafe/cafe_search.html'

    def get_queryset(self):
        keywords = self.request.GET.get('search-term', None)
        if keywords:
            qs = Cafe.objects.all()
            for keyword in keywords.split():
                qs = qs.filter(name__icontains=keyword)
        else:
            qs = Cafe.objects.none()
        return qs
