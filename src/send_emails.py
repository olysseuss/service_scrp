import json
import os, sys
import django
import datetime

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()

from django.contrib.auth import get_user_model
from scrap.models import Vacancy, Error, Url
from django.core.mail import EmailMultiAlternatives
from scraping_service.settings import EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Вакансии на {today}'
text_content = 'Рассылка вакансий'
from_email = EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

# send emails with vacancies
User = get_user_model()
# selection of all active users, where the key is city and language
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
    qs = Vacancy.objects.filter(**params, timestamp__year=today.year, timestamp__month=today.month, timestamp__day=today.day).values()
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
subject_err = ''
text_content_err = ''
to = ADMIN_USER
_html_err = ''

qs = Error.objects.filter(timestamp=today)
if qs.exists():
    error = qs.first()  # one entry for one date
    # formation of a letter with errors
    data = error.data.get('errors', [])  # get values for key 'errors' in json-string
    # data = json.loads(j_data)  # convert json-string to list
    if data:
        for i in data:
            _html_err += f' <p><a href="{i["url"]}">Error: {i["title"]} </a></p>'
        subject_err = f'Ошибки скрапинга на {today}'
        text_content_err = 'Ошибки скрапинга'
    # formation of a letter with a user's wish
    data = error.data.get('user_data')
    if data:
        _html_err += '<hr>'
        for i in data:
            _html_err += f' <p>Город: {i["city"]}. Специальность: {i["language"]}. Email: {i["email"]}.</p>'
        subject_err = f'Пожелание пользователя {today}'
        text_content_err = 'Пожелание пользователя'

# send emails with missing urls
# selection of all active urls, where the key is city and language
qs = Url.objects.all().values('id_city', 'id_language')
urls_dict = {(i['id_city'], i['id_language']): True for i in qs}
missing_urls = ''
for keys in users_dict:
    if keys not in urls_dict:
        if keys[0] and keys[1]:
            missing_urls += f' <p>Для {keys[0]} и {keys[1]} отсутствуют ссылки на целевые сайты.</p>'
if missing_urls:
    subject_err += "Отсутствие ссылок"
    text_content_err += "Отсутствие ссылок"
    _html_err += missing_urls
if subject_err:
    msg = EmailMultiAlternatives(subject_err, text_content_err, from_email, [to])
    msg.attach_alternative(_html_err, "text/html")
    msg.send()
