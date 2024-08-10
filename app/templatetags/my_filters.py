import datetime
from django import template
from django.utils import timezone
from app import models

register = template.Library()
today = timezone.now().date()

@register.filter()
def addDays(days):
    newDate = datetime.date.today() + datetime.timedelta(days=days)
    return newDate

@register.simple_tag()
def total_users():
    return models.User.objects.count()

@register.simple_tag()
def todays_events():
    return models.Event.objects.filter(date=today).count()

@register.simple_tag()
def todays_users():
    return models.User.objects.filter(date_joined__date=today).count()