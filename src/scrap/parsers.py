import requests
from bs4 import BeautifulSoup as BS
from random import randint


__all__ = ('work_ua', 'rabota_ua', 'dou_ua', 'djinni_co')

headers = [
    {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'},
    {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 OPR/70.0.3728.189',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'},
    {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'},

]


def work_ua(url):
    jobs = []
    errors = []
    # url = 'https://www.work.ua/ru/jobs-zaporizhzhya-python/'
    domain = 'https://www.work.ua'
    resp = requests.get(url=url, headers=headers[randint(0, 2)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id="pjax-job-list")
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_list:
                title = div.find('h2')
                href = title.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': "Div with id 'pjax-job-list' does not exist"})
    else:
        errors.append({'url': url, 'title': 'Page do not response', 'code': resp.status_code})
    return jobs, errors


def rabota_ua(url):
    jobs = []
    errors = []
    # url = 'https://rabota.ua/zapros/python/днепропетровск'
    domain = 'https://rabota.ua/'
    resp = requests.get(url=url, headers=headers[randint(0, 2)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_table_non = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
        if not main_table_non:
            main_table = soup.find('table', id="ctl00_content_vacancyList_gridList")
            if main_table:
                tr_list = main_table.find_all('tr', attrs={'id': True})
                for tr in tr_list:
                    div = tr.find('div', attrs={'class': 'card-body'})
                    if div:
                        title = div.find('p', attrs={'class': 'card-title'})
                        href = title.a['href']
                        content = div.find('div', attrs={'class': 'card-description'}).text
                        company = 'No name'
                        p_tag = div.find('p', attrs={'class': 'company-name'})
                        if p_tag:
                            company = p_tag.a.text
                        jobs.append(
                            {'title': title.text, 'url': domain + href, 'description': content, 'company': company})
            else:
                errors.append(
                    {'url': url, 'title': "Table with id 'ctl00_content_vacancyList_gridList' does not exist"})
        else:
            errors.append({'url': url, 'title': "Page is empty"})
    else:
        errors.append({'url': url, 'title': 'Page do not response', 'code': resp.status_code})
    return jobs, errors


def dou_ua(url):
    jobs = []
    errors = []
    # url = 'https://jobs.dou.ua/vacancies/?category=Python&search=Днепр'
    domain = 'https://jobs.dou.ua/'
    resp = requests.get(url=url, headers=headers[randint(0, 2)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id="vacancyListId")
        if main_div:
            li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
            for li in li_list:
                title = li.find('div', attrs={'class': 'title'})
                href = title.a['href']
                content = li.find('div', attrs={'class': 'sh-info'}).text
                company = 'No name'
                a = title.find('a', attrs={'class': 'company'})
                if a:
                    company = a.text
                jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': "Div with id 'pjax-job-list' does not exist"})
    else:
        errors.append({'url': url, 'title': 'Page do not response', 'code': resp.status_code})
    return jobs, errors


def djinni_co(url):
    jobs = []
    errors = []
    # url = 'https://djinni.co/jobs/keyword-python/zaporizhzhya/'
    domain = 'https://djinni.co'
    resp = requests.get(url=url, headers=headers[randint(0, 2)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
        if main_ul:
            li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
            for div in li_list:
                title = div.find('div', attrs={'class': 'list-jobs__title'})
                href = title.a['href']
                content = div.find('div', attrs={'class': 'list-jobs__description'}).text
                company = 'No name'
                comp = div.find('div', attrs={'class': 'list-jobs__details__info'})
                if comp:
                    company = comp.find_all('a')[1].text
                jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': "Div with id 'pjax-job-list' does not exist"})
    else:
        errors.append({'url': url, 'title': 'Page do not response', 'code': resp.status_code})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://djinni.co/jobs/keyword-python/zaporizhzhya/'
    jobs, errors = djinni_co(url)
    with open('../work.txt', 'w', encoding='utf-8') as f_work:
        f_work.write(str(jobs))
