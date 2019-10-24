from django.db import models


class Player(models.Model):
    pass


class Game(models.Model):
    guessed_number = models.IntegerField(verbose_name='Загаданное число')
    player = models.ManyToManyField('Player', related_name='game', through='PlayerGameInfo')
    active = models.BooleanField(verbose_name='Активная', default=True)


class PlayerGameInfo(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE, verbose_name='Игрок')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='Игра')
    is_creator = models.BooleanField(verbose_name='Автор игры')
    attempts = models.IntegerField(verbose_name='Количество попыток')