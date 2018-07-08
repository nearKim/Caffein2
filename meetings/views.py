from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import (
    Meeting,
    OfficialMeeting,
    CoffeeEducation,
    CoffeeMeeting
)