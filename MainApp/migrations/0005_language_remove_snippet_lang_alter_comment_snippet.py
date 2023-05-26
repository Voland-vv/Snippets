# Generated by Django 4.1.1 on 2023-05-26 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0004_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=32)),
                ('short_name', models.CharField(max_length=8)),
            ],
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='lang',
        ),
        migrations.AlterField(
            model_name='comment',
            name='snippet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='MainApp.snippet'),
        ),
    ]
