# Generated by Django 4.2.6 on 2023-10-27 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ripple_predict', '0002_alter_socialmediapost_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prediction',
            options={'verbose_name': 'Prediction', 'verbose_name_plural': 'Predictions'},
        ),
        migrations.CreateModel(
            name='Embedding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment', models.CharField(db_index=True, max_length=64)),
                ('response', models.TextField()),
                ('embeddings', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('smp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ripple_predict.socialmediapost')),
            ],
            options={
                'verbose_name': 'Embedding',
                'verbose_name_plural': 'Embeddings',
            },
        ),
    ]