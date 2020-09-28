from scrap.parsers import *

parsers = (
    (work_ua, 'https://www.work.ua/ru/jobs-zaporizhzhya-python/'),
    (rabota_ua, 'https://rabota.ua/zapros/python/запорожье'),
    (dou_ua, 'https://jobs.dou.ua/vacancies/?category=Python&search=Запорожье'),
    (djinni_co, 'https://djinni.co/jobs/keyword-python/zaporizhzhya/'),
)

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

with open('work.txt', 'w', encoding='utf-8') as f_work:
    f_work.write(str(jobs))
