# Generated by Django 3.2.16 on 2024-06-18 18:24

import cheonbaeksa.bases.models
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='삭제 여부')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='삭제 시간')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='활성화 여부')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('user_id', models.IntegerField(verbose_name='유저 ID')),
                ('order_id', models.IntegerField(verbose_name='주문 ID')),
                ('imp_uid', models.CharField(blank=True, max_length=20, null=True, verbose_name='포트원 결제 UID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='총 가격')),
                ('status', model_utils.fields.StatusField(choices=[('PREPARED', '결제 예정'), ('FAILED', '결제 실패'), ('PAID', '결제 완료'), ('PARTIAL_CANCELLED', '부분 취소'), ('CANCELLED', '전체 취소')], default=None, max_length=100, no_check_for_status=True, null=True, verbose_name='상태')),
                ('prepared_at', model_utils.fields.MonitorField(default=None, monitor='status', null=True, verbose_name='결제 예정 시간', when={'PREPARED'})),
                ('failed_at', model_utils.fields.MonitorField(default=None, monitor='status', null=True, verbose_name='결제 실패 시간', when={'FAILED'})),
                ('paid_at', model_utils.fields.MonitorField(default=None, monitor='status', null=True, verbose_name='결제 완료 시간', when={'PAID'})),
                ('partial_cancelled_at', model_utils.fields.MonitorField(default=None, monitor='status', null=True, verbose_name='부분 취소 시간', when={'PARTIAL_CANCELLED'})),
                ('cancelled_at', model_utils.fields.MonitorField(default=None, monitor='status', null=True, verbose_name='전체 취소 시간', when={'CANCELLED'})),
                ('pg_data', models.JSONField(null=True, verbose_name='PG 데이터')),
            ],
            options={
                'verbose_name': '결제',
                'verbose_name_plural': '결제',
                'ordering': ['-created'],
            },
            bases=(cheonbaeksa.bases.models.UpdateMixin, models.Model),
        ),
    ]
