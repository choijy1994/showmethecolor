# Generated by Django 2.1.7 on 2019-05-08 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageUpload', '0004_auto_20190508_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cosmetics',
            fields=[
                ('name', models.CharField(default='', max_length=50, primary_key=True, serialize=False)),
                ('brand', models.CharField(default='', max_length=50)),
                ('R', models.IntegerField()),
                ('G', models.IntegerField()),
                ('B', models.IntegerField()),
            ],
        ),
    ]
