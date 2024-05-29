# Django
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# DRF
from rest_framework.authtoken.models import Token

# Constants
from cheonbaeksa.apps.wedding_budgets.constants import wedding_budget_data
from cheonbaeksa.apps.wedding_checks.constants import wedding_check_data
from cheonbaeksa.apps.wedding_schedules.constants import wedding_schedule_data

# Models
from cheonbaeksa.apps.wedding_budgets.models import WeddingBudget
from cheonbaeksa.apps.alarms.models import Alarm, AlarmGroup
from cheonbaeksa.apps.users.models.index import User
from cheonbaeksa.apps.wedding_budget_users.models import WeddingBudgetUser
from cheonbaeksa.apps.wedding_check_users.models import WeddingCheckUser
from cheonbaeksa.apps.wedding_checks.models import WeddingCheck
from cheonbaeksa.apps.wedding_schedule_users.models import WeddingScheduleUser
from cheonbaeksa.apps.wedding_schedules.models import WeddingSchedule


# Main Section
@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    print('========== User post_save: Create Token, AlarmGroup ==========')

    if created:
        # Create Token
        Token.objects.create(user=instance)

        # Create AlarmGroup
        alarm_group = AlarmGroup.objects.create(user=instance)

        # Create Alarm
        if not instance.username:
            content = '푸딩 가입을 축하드립니다! 푸딩에서 결혼을 계획해보세요!'
        else:
            content = f'{instance.username}님 푸딩 가입을 축하드립니다! 푸딩에서 결혼을 계획해보세요!'

        Alarm.objects.create(alarm_group=alarm_group, user=instance, content=content, is_notice=True)


@receiver(pre_save, sender=User)
def cache_image(sender, instance, *args, **kwargs):
    print('========== User pre_save: Image ==========')

    profile_image = None

    if instance.id:
        user = User.objects.get(id=instance.id)
        profile_image = user.profile_image

    instance.__profile_image = profile_image


@receiver(post_save, sender=User)
def image_update(sender, instance, created, **kwargs):
    print('========== User post_save: Image ==========')

    if instance.__profile_image != instance.profile_image:

        # Update ProfileImageUrl
        if instance.profile_image:
            instance.profile_image_url = instance.profile_image.url
            instance.save(update_fields=['profile_image_url'])


# 기본 체크 데이터 생성
@receiver(post_save, sender=User)
def create_wedding_check(sender, instance, created, **kwargs):
    print('========== User post_save: Create WeddingCheck ==========')

    if created:
        code = wedding_check_data[0]['code']

        wedding_check = WeddingCheck.objects.create(user=instance, code=code)
        wedding_check_user = WeddingCheckUser.objects.create(user=instance, wedding_check=wedding_check,
                                                             permission='HOST')
        print('wedding_check.id : ', wedding_check.id)
        print('wedding_check_user : ', wedding_check_user)


# 기본 예산 데이터 생성
@receiver(post_save, sender=User)
def create_wedding_budget(sender, instance, created, **kwargs):
    print('========== User post_save: Create WeddingBudget ==========')

    if created:
        code = wedding_budget_data[0]['code']

        wedding_budget = WeddingBudget.objects.create(user=instance, code=code)
        wedding_budget_user = WeddingBudgetUser.objects.create(user=instance,
                                                               wedding_budget=wedding_budget,
                                                               permission='HOST')
        print('wedding_budget.id : ', wedding_budget.id)
        print('wedding_budget_user : ', wedding_budget_user)


# 기본 스케줄 데이터 생성
@receiver(post_save, sender=User)
def create_wedding_schedule(sender, instance, created, **kwargs):
    print('========== User post_save: Create WeddingSchedule ==========')

    if created:
        code = wedding_schedule_data[0]['code']

        wedding_schedule = WeddingSchedule.objects.create(user=instance, code=code)
        wedding_schedule_user = WeddingScheduleUser.objects.create(user=instance,
                                                                   wedding_schedule=wedding_schedule,
                                                                   permission='HOST')
        print('wedding_schedule.id : ', wedding_schedule.id)
        print('wedding_schedule_user : ', wedding_schedule_user)
