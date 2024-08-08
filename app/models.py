from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User fields: first_name, last_name, email, username, password

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    profile_picture = models.ImageField(default='default_profile_picture.jpg', upload_to='profile_pictures')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Sport(models.Model):
    name = models.CharField(max_length=128)


class Facility(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    sport = models.ForeignKey(Sport, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.name} {self.sport.name}'


class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    facility = models.ForeignKey(Facility, on_delete=models.DO_NOTHING)
    date = models.DateField(default="")
    time = models.TimeField(default="")
    estimated_time = models.IntegerField(choices=((30, "30"), (45, "45"), (60, "60"), (75, "75"), (90, "90"),
                                                  (105, "105"), (120, "120"), (135, "135"), (150, "150")))
    max_participants = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(Profile, blank=True)