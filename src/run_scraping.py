import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scrap.parsers import *
from scrap.models import Vacancy, City, Language
from django.db import DatabaseError

parsers = (
    (work_ua, 'https://www.work.ua/ru/jobs-zaporizhzhya-python/'),
    (rabota_ua, 'https://rabota.ua/zapros/python/запорожье'),
    (dou_ua, 'https://jobs.dou.ua/vacancies/?category=Python&search=Запорожье'),
    (djinni_co, 'https://djinni.co/jobs/keyword-python/zaporizhzhya/'),
)

city = City.objects.filter(slug='zaporizhzhya').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    vac = Vacancy(**job, id_city=city, id_language=language)
    try:
        vac.save()
    except DatabaseError:
        pass

# with open('work.txt', 'w', encoding='utf-8') as f_work:
#     f_work.write(str(jobs))
