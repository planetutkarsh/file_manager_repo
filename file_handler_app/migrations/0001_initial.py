# Generated by Django 2.0.6 on 2018-07-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('path', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'document',
            },
        ),
        migrations.CreateModel(
            name='UserDirectory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directory_path', models.CharField(max_length=100)),
                ('crt_dt', models.DateTimeField(auto_now_add=True)),
                ('upd_dt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user_directory',
            },
        ),
    ]
