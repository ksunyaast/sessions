# Generated by Django 2.1.5 on 2019-10-23 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guessed_number', models.IntegerField(verbose_name='Загаданное число')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerGameInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_creator', models.BooleanField(verbose_name='Автор игры')),
                ('attempts', models.IntegerField(verbose_name='Количество попыток')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game', verbose_name='Игра')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Player', verbose_name='Игрок')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='player',
            field=models.ManyToManyField(related_name='player', through='game.PlayerGameInfo', to='game.Player'),
        ),
    ]