# Generated by Django 4.2.6 on 2023-10-20 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ripple_predict', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialmediapost',
            options={'verbose_name': 'SocialMediaPost', 'verbose_name_plural': 'SocialMediaPosts'},
        ),
        migrations.RenameField(
            model_name='prediction',
            old_name='algo',
            new_name='experiment',
        ),
    ]
