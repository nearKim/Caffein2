from cafe.models import Cafe
from django.views.generic import ListView, DetailView, CreateView
from django.http import JsonResponse


class CafeListView(ListView):
    model = Cafe
    template_name = 'cafe/cafe_list.html'

    def get_queryset(self):
        return Cafe.objects.filter()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CafeListView, self).get_context_data(**kwargs)
        # context['aaa'] = 'bbb'
        return context


class CafeDetailView(DetailView):
    model = Cafe


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class CafeCreateView(AjaxableResponseMixin, CreateView):
    model = Cafe
    fields = '__all__'

