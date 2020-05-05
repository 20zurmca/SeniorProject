# Generated by Django 3.0.3 on 2020-04-25 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_auto_20200424_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='documents',
            name='sqlFile',
        ),
        migrations.AlterField(
            model_name='documents',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]