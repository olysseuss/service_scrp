from django.shortcuts import render
from .models import Vacancy


def home(requests):
    qs = Vacancy.objects.all()
    return render(requests, 'home.html', {'object_list': qs})
