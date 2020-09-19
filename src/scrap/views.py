from django.shortcuts import render
from .models import Vacancy


def home(requests):
    print(requests.GET)
    city = requests.GET.get('city')
    language = requests.GET.get('language')
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['id_city__name'] = city
        if language:
            _filter['id_language__name'] = language
        qs = Vacancy.objects.filter(**_filter)
    return render(requests, 'scrap/home.html', {'object_list': qs})
