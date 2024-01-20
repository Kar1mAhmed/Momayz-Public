from django.contrib import admin
from .models import QA


admin.site.register(QA) 



########## UN REGISTER SOME USELESS MODELS FOR ADMIN ######################

# print(admin.site._registry)        TO GET ALL REGISTERED MODELS

from django.contrib.sites.models import Site
from django_celery_results.models import TaskResult, GroupResult
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule, PeriodicTask
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken


admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)

admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.unregister(EmailAddress)

admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)


admin.site.unregister(Site)



admin.site.site_header = 'Momayz Admin'

