# Generated by Django 5.1.3 on 2024-11-26 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_passing', '0004_alter_testsession_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_passing.answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_passing.question')),
                ('test_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_passing.testsession')),
            ],
            options={
                'unique_together': {('test_session', 'question')},
            },
        ),
    ]
