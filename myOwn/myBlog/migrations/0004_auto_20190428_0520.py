# Generated by Django 2.2 on 2019-04-28 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myBlog', '0003_post_like_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like_num',
            field=models.IntegerField(default=-1),
        ),
    ]
