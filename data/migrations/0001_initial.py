# Generated by Django 3.0.6 on 2020-11-06 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Polygon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('coordinates', models.CharField(max_length=1500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='polygon', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]