# Django
from django.db.models.signals import post_save
from django.dispatch import receiver

# DRF
from rest_framework.authtoken.models import Token

# Models
from cheonbaeksa.apps.users.models.index import User


# Main Section
@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    print('========== User post_save: Create Token ==========')

    if created:
        # Create Token
        Token.objects.create(user=instance)
