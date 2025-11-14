from django.db import models as m
from django.contrib.auth.models import AbstractUser
from django.conf import settings

PAMAINA = (
        ('1', "Dieninė"),
        ('2', "Vakarinė"),
        ('3', "Naktinė"),
    )
TASK_STATUS = (
        ('a', "Atlikta"),
        ('p', "Pavėluota"),
        ('n', "Neatlikta"),
    )
class CustomUser(AbstractUser):
    first_name = m.CharField(verbose_name="Vardas")
    last_name = m.CharField(verbose_name="Pavardė")
    shift = m.CharField(verbose_name="Pamaina", max_length=1, choices=PAMAINA,
                        default='1',)
    
    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.title()

        if self.last_name:
            self.last_name = self.last_name.title()    
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Darbuotojas"
        verbose_name_plural = "Darbuotojai"

    def __str__(self):
        return f"{self.username}"

# Perkelt user ir date į UzduotisInstance. Prideti komentarus UzduotisInstance ir prie User

class Uzduotis(m.Model):
    name = m.CharField(verbose_name="Pavadinimas")
    content = m.TextField(verbose_name="Aprašymas")
    date = m.DateTimeField(verbose_name="Sukūrimo data", auto_now_add=True)
    user = m.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name="Kieno sukurta",
                        on_delete=m.SET_NULL, null=True, blank=True)
    shift = m.CharField(verbose_name="Pamaina", max_length=1, choices=PAMAINA,
                          default='1',)
    
    class Meta:
        verbose_name = "Užduotis"
        verbose_name_plural = "Užduotys"

    def __str__(self):
        return self.name

class UzduotisInstance(m.Model):
    date = m.DateTimeField(verbose_name="Sukūrimo data", auto_now_add=True)
    user = m.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name="Kieno sukurta",
                        on_delete=m.SET_NULL, null=True, blank=True)

    task = m.ForeignKey(to="Uzduotis",
                        verbose_name="Užduotis",
                        on_delete=m.CASCADE,
                        related_name="instances")
    worker = m.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name="Darbuotojas",
                               related_name="tasks")
    due_date = m.DateTimeField(verbose_name="Padaryti iki", null=True, blank=True)
    
    def display_worker(self):
        return ", ".join(worker.username for worker in self.worker.all())
    
    display_worker.short_description = "Darbuotojas"

    status = m.CharField(verbose_name="Statusas", max_length=1, choices=TASK_STATUS,
                         default='n', blank=True)
    
    class Meta:
        verbose_name = "Dienos užduotis"
        verbose_name_plural = "Dienos užduotys"

    def __str__(self):
        return f"{self.task.name}"


