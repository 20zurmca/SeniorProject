# Generated by Django 3.0.3 on 2020-03-28 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HighSchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('institution', models.CharField(max_length=100)),
                ('stateOrProvince', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(max_length=50)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('schoolType', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MatchedHighSchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rosterYear', models.IntegerField()),
                ('playerNumber', models.IntegerField(null=True)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('year', models.CharField(max_length=10)),
                ('position1', models.CharField(max_length=20)),
                ('height', models.CharField(max_length=10, null=True)),
                ('weight', models.IntegerField(null=True)),
                ('homeTown', models.CharField(max_length=30, null=True)),
                ('stateOrCountry', models.CharField(max_length=20, null=True)),
                ('highSchool', models.CharField(max_length=100, null=True)),
                ('alternativeSchool', models.CharField(max_length=50, null=True)),
                ('college', models.CharField(max_length=50)),
                ('collegeLeague', models.CharField(max_length=50)),
                ('bioLink', models.CharField(max_length=100)),
                ('isStarter', models.CharField(max_length=1, null=True)),
                ('accolade', models.CharField(max_length=20, null=True)),
                ('matchedCity', models.CharField(max_length=30, null=True)),
                ('matchedInstitution', models.CharField(max_length=30, null=True)),
                ('matchedStateProvince', models.CharField(max_length=20, null=True)),
                ('matchedCountry', models.CharField(max_length=20, null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('schoolType', models.CharField(max_length=13, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RosterMasterData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rosterYear', models.IntegerField()),
                ('playerNumber', models.IntegerField(null=True)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('year', models.CharField(max_length=10)),
                ('position1', models.CharField(max_length=20)),
                ('height', models.CharField(max_length=10, null=True)),
                ('weight', models.IntegerField(null=True)),
                ('homeTown', models.CharField(max_length=30, null=True)),
                ('stateOrCountry', models.CharField(max_length=20, null=True)),
                ('highSchool', models.CharField(max_length=100, null=True)),
                ('alternativeSchool', models.CharField(max_length=50, null=True)),
                ('college', models.CharField(max_length=50)),
                ('collegeLeague', models.CharField(max_length=50)),
                ('bioLink', models.CharField(max_length=100)),
                ('isStarter', models.CharField(max_length=1, null=True)),
                ('accolade', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
