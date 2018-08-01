from cafe.models import Cafe
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    num_cafes = Cafe.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_cafes': num_cafes,
        'num_visits': num_visits,
    }
    return render(request, 'cafe/index.html', context=context)


class CafeListView(ListView):
    model = Cafe
    template_name = 'cafe/cafe_list.html'
    '''
    def get_queryset(self):
        return Cafe.objects.filter()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CafeListView, self).get_context_data(**kwargs)
        # context['aaa'] = 'bbb'
        return context'''


class CafeDetailView(DetailView):
    model = Cafe
    template_name = 'cafe/cafe_detail.html'


class CafeDeleteView(DeleteView):
    model = Cafe
    success_url = '/cafe/'
    template_name = 'cafe/cafe_delete.html'


class CafeUpdataView(UpdateView):
    model = Cafe
    fields = ['name', 'address', 'description', 'phone', 'machine', 'grinder', 'price', 'from_time', 'to_time',
              'closed_day', 'closed_frq', 'closed_holiday', 'image']
    success_url = '/cafe/'
    template_name = 'cafe/cafe_update.html'


class CafeCreateView(CreateView):
    model = Cafe
    fields = ['name', 'address', 'description', 'phone', 'machine', 'grinder', 'price', 'from_time', 'to_time',
              'closed_day', 'closed_frq', 'closed_holiday', 'image']
    success_url = '/cafe/'
    template_name = 'cafe/cafe_create.html'

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super(CafeCreateView, self).form_valid(form)


