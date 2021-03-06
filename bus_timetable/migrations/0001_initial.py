# Generated by Django 3.2.3 on 2021-06-10 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bus_line', '0001_initial'),
        ('bus_pair', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusTimetable',
            fields=[
                ('id',
                 models.BigAutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('departure_at',
                 models.DateTimeField(
                     verbose_name='出発日時')),
                ('arrive_at',
                 models.DateTimeField(
                     verbose_name='到着日時')),
                ('created_at',
                 models.DateTimeField(
                     auto_now_add=True,
                     verbose_name='登録日時')),
                ('bus_line',
                 models.ForeignKey(
                     db_constraint=False,
                     on_delete=django.db.models.deletion.PROTECT,
                     related_name='bus_line',
                     to='bus_line.busline',
                     verbose_name='バス路線')),
                ('bus_pair',
                 models.ForeignKey(
                     db_constraint=False,
                     on_delete=django.db.models.deletion.PROTECT,
                     related_name='bus_pair',
                     to='bus_pair.buspair',
                     verbose_name='バス停組み合わせ')),
            ],
            options={
                'verbose_name': 'バス時刻',
                'verbose_name_plural': 'バス時刻',
                'db_table': 'bus_timetable',
                'ordering': ['created_at'],
            },
        ),
    ]
