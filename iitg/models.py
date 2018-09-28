from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class Page(models.Model):

    name=models.TextField(max_length=2000, help_text="Enter page name")

    event = models.ManyToManyField(Event)

    def get_absolute_url(self):
        return reverse('page-detail', args=[str(self.id)])

    def __str__(self):
        return "%s" % (self.name)


class Event(models.Model):

    name=models.TextField(max_length=2000, help_text="Enter event name")

    time = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])

    def __str__(self):
        return "%s" % (self.name)

class Student(models.Model):

    user=models.OneToOneField(User,help_text="a",related_name='student')

    rollNo=models.IntegerField(required=True,help_text="Enter your IITG roll No.")

    pages = models.ManyToManyField(Page, help_text='Select page(s) which you want to subscribe')
    
    activeEvent=models.ForeignKey(Event, related_name="events", on_delete=models.CASCADE, help_text="a")


class Admin(models.Model):

    user=models.OneToOneField(User,help_text="a",related_name='admin')

    rollNo=models.IntegerField(required=True,help_text="Enter your IITG roll No.")

    pages = models.ManyToManyField(Page, help_text='Select page(s) which you want to subscribe')