# Generated by Django 2.2 on 2019-05-04 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myBlog', '0008_post_favorites'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to='myBlog.Tag'),
        ),
    ]
