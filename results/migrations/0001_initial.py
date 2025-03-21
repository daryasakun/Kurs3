# Generated by Django 5.1.3 on 2024-11-25 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('test_passing', '0001_initial'),
        ('users', '0003_alter_student_managers_alter_teacher_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('result_id', models.AutoField(primary_key=True, serialize=False)),
                ('number_of_points', models.IntegerField()),
                ('date_of_passing', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_passing.test')),
            ],
            options={
                'verbose_name': 'Результат',
                'verbose_name_plural': 'Результаты',
                'db_table': 'results',
            },
        ),
    ]
