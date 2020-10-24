import asyncio
import os, sys, datetime

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scrap.parsers import *
from scrap.models import Vacancy, City, Language, Error, Url
from django.db import DatabaseError
from django.contrib.auth import get_user_model

User = get_user_model()  # returns the default user


def user_get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['id_city_id'], q['id_language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dct:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dct[pair]
            urls.append(tmp)
    return urls


jobs, errors = [], []


async def async_main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    jobs.extend(job)
    errors.extend(err)


user_settings = user_get_settings()
url_list = get_urls(user_settings)

parsers = (
    (work_ua, 'work'),
    (rabota_ua, 'rabota'),
    (dou_ua, 'dou'),
    (djinni_co, 'djinni'),
)

# city = City.objects.filter(slug='zaporizhzhya').first()
# language = Language.objects.filter(slug='python').first()


loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(async_main(f)) for f in tmp_tasks])

# for data in url_list:
#
#     for func, key in parsers:
#         url = data['url_data'][key]
#         # start scraping functions
#         j, e = func(url, id_city=data['city'], id_language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    vac = Vacancy(**job)
    try:
        vac.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=datetime.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        err = Error(data=f'errors: {errors}').save()

# with open('work.txt', 'w', encoding='utf-8') as f_work:
#     f_work.write(str(jobs))
