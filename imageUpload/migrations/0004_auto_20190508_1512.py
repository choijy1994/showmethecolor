# Generated by Django 2.1.7 on 2019-05-08 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageUpload', '0003_auto_20190508_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='modifiedmodel',
            name='tone',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='uploadfilemodel',
            name='tone',
            field=models.CharField(default='', max_length=10),
        ),
    ]
