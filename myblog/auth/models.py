from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE,
                                related_name='profile')
    org = models.CharField('Organization', max_length=128, blank=True)
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    mod_data = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User profile'

    def __str__(self):
        return f"{self.user.__str__()}"
