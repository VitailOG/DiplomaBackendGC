# Generated by Django 4.0.1 on 2022-06-23 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_studentsource_created_at_studentsource_type_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
    ]
