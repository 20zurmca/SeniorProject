# Generated by Django 3.0.3 on 2020-03-13 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20200312_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highschool',
            name='stateOrProvince',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='rostermasterdata',
            name='accolade',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='rostermasterdata',
            name='alternativeSchool',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rostermasterdata',
            name='height',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='rostermasterdata',
            name='highSchool',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rostermasterdata',
            name='homeTown',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='rostermasterdata',
            name='isStarter',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='rostermasterdata',
            name='playerNumber',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='rostermasterdata',
            name='stateOrCountry',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='rostermasterdata',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]