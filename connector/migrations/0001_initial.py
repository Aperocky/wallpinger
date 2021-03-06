# Generated by Django 2.0.5 on 2018-06-02 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ping_time', models.DateTimeField(verbose_name='time pinged')),
                ('ping_result', models.DecimalField(decimal_places=3, max_digits=7)),
                ('ping_success', models.PositiveSmallIntegerField()),
                ('ping_total', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_name', models.CharField(max_length=50)),
                ('website_url', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='website_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connector.Website'),
        ),
    ]
