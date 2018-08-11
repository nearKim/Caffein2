from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

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


