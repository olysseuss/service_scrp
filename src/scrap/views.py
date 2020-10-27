from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .forms import FindForm
from .models import Vacancy


def home_view(request):
    #print(request.GET)
    form = FindForm()
    return render(request, 'scrap/home.html', {'form': form})

def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = {}
        if city:
            _filter['id_city__slug'] = city
        if language:
            _filter['id_language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 5) #show 10 cards per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scrap/list.html', context)

def detail_view(request, pk=None):
    # object_ = Vacancy.objects.get(pk=pk)
    object_ = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'scrap/detail.html', {'object': object_})
