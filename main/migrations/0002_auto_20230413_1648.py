# Generated by Django 3.2.18 on 2023-04-13 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodpackage',
            name='FoodIteminPackage',
        ),
        migrations.AddField(
            model_name='foodpackage',
            name='FoodIteminPackage',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.fooditem'),
        ),
    ]
