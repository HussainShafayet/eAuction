# Generated by Django 2.2 on 2021-05-19 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0008_auto_20210519_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_item',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]