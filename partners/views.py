from django.shortcuts import render
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.views.generic import View, DetailView
from .models import (
    PartnerMeeting,
    Partners
)


class PartnerDetailView(DetailView):
    model = Partners