import os, sys
import django
import datetime

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()

from django.contrib.auth import get_user_model
from scrap.models import Vacancy, Error
from django.core.mail import EmailMultiAlternatives
from scraping_service.settings import EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Вакансии на {today}'
text_content = 'Рассылка вакансий'
from_email = EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

# send emails with vacancies
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for i in qs:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'], i['language'])].append(i['email'])
if users_dict:
    params = {'id_city_id__in': [], 'id_language_id__in': []}  # __in - find all values belonging to this pair
    for pair in users_dict.keys():
        params['id_city_id__in'].append(pair[0])
        params['id_language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['id_city_id'], i['id_language_id']), [])
        vacancies[(i['id_city_id'], i['id_language_id'])].append(i)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f' <h5><a href="{row["url"]}">{row["title"]} - {row["company"]}</a></h5>'
            html += f' <p>{row["description"]}</p><br><hr>'
            # html += f' <p>{row["timestamp"]}</p><br><hr>'
        _html = html if html else '<h2>По вашему запросу на данный момент нет данных</h2>'

        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

# send emails with errors
qs = Error.objects.filter(timestamp=today)
if qs.exists():
    error = qs.first()  # one entry for one date
    data = error.data
    _html_err = ''
    for i in data:
        _html_err += f' <p><a href="{i["url"]}">Error: {i["title"]} </a></p>'

    subject_err = f'Ошибки скрапинга на {today}'
    text_content_err = 'Ошибки скрапинга'
    to = ADMIN_USER
    msg = EmailMultiAlternatives(subject_err, text_content_err, from_email, [to])
    msg.attach_alternative(_html_err, "text/html")
    msg.send()

