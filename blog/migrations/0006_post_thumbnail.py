# Generated by Django 4.2.9 on 2024-02-04 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
