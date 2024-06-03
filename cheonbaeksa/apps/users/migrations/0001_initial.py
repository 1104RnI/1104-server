# Generated by Django 3.2.16 on 2024-06-03 17:13

import cheonbaeksa.apps.users.models.fields.phone_number
import cheonbaeksa.apps.users.models.managers.objects
import cheonbaeksa.bases.models
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='삭제 여부')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='삭제 시간')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.EmailField(error_messages={'unique': '이미 사용중인 이메일 입니다.'}, max_length=254, unique=True, verbose_name='이메일')),
                ('phone', cheonbaeksa.apps.users.models.fields.phone_number.PhoneNumberField(blank=True, max_length=20, region=None, verbose_name='전화')),
                ('username', models.CharField(blank=True, max_length=20, verbose_name='닉네임')),
                ('is_email_verified', models.BooleanField(default=False, verbose_name='이메일 인증 여부')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '유저',
                'verbose_name_plural': '유저',
                'ordering': ['-created'],
            },
            bases=(cheonbaeksa.bases.models.UpdateMixin, models.Model),
            managers=[
                ('objects', cheonbaeksa.apps.users.models.managers.objects.UserMainManager()),
            ],
        ),
    ]
