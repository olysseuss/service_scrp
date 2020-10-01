import jsonfield as jsonfield
from django.db import models

from scrap.utils import from_cyrillic_to_eng


def default_urls():
    return {'work': '', 'rabota': '', 'dou': '', 'djinni': ''}


class City(models.Model):
    name = models.CharField(max_length=80, verbose_name='Название города', unique=True)
    slug = models.CharField(max_length=50, blank=True, verbose_name='Слаг', unique=True)

    class Meta:
        verbose_name = 'Название города'
        verbose_name_plural = 'Названия городов'

    def __str__(self):
        return self.name

    # autocomplete line 'slug'
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Язык программирования', unique=True)
    slug = models.CharField(max_length=50, blank=True, verbose_name='Слаг', unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Название вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    timestamp = models.DateTimeField(auto_now_add=True)
    id_city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    id_language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp'] # where '-' is DESC

    def __str__(self):
        return '{0} , {1}'.format(self.title, self.company)


class Error(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = jsonfield.JSONField()

    def __str__(self):
        return self.timestamp


class Url(models.Model):
    id_city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    id_language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ('id_city', 'id_language')  # unique key : id_city+id_language
