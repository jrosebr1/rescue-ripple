# Generated by Django 4.2.6 on 2023-10-30 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ripple_predict', '0003_alter_prediction_options_embedding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='embedding',
            name='embeddings',
        ),
    ]
