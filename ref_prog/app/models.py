from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
# Create your models here.


def get_unique_code():
    code = str(uuid.uuid4()).replace('-', '')[:10]
    return code


class user_info(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        default='defaultUser.png', null=True, blank=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    ref_code = models.CharField(max_length=10, default=get_unique_code())
    referred_by_up = models.CharField(null=True, blank=True, max_length=20)
    referred_by_down = models.CharField(max_length=20, null=True, blank=True)
    has_helped_up = models.BooleanField(default=False)
    has_helped_down = models.BooleanField(default=False)
    sharing_increased = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

    def set(self, arg1, arg2):
        self.referred_by_up = arg1
        self.referred_by_down = arg2
        super().save()

    def has_helped_up_tick(self):
        self.has_helped_up = True
        super().save()

    def has_helped_down_tick(self):
        self.has_helped_down = True
        super().save()

    def sharing_increaser(self):
        self.sharing_increased = self.sharing_increased + 1
        super().save()


def create_info(sender, **kwargs):
    if kwargs['created']:
        User_Info = user_info.objects.create(user=kwargs['instance'])


post_save.connect(create_info, sender=User)
