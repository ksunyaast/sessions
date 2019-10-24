from django.shortcuts import render
from game.forms import MakeNumber, CheckNumber
from game.models import Player, Game, PlayerGameInfo


def show_home(request):
    player_id = request.session.get('player_id')
    game_id = request.session.get('game_id')
    player_game_info = PlayerGameInfo.objects.all()
    player = Player.objects.all()
    game = Game.objects.all()

    # проверка, есть ли активная игра
    if len(game.filter(active=True)):
        active_game = game.filter(active=True)[0]
    else:
        active_game = None

    number_msg = None
    info_msg = None
    main_msg = None

    # если в сессии нет player_id, то создаем нового игрока в бд и сохраняем id в сессию player_id
    # устанавливаем переменную this_player для работы в дальнейшем, в которой хранится текущий игрок
    if not player_id:
        this_player = Player.objects.create()
        request.session['player_id'] = this_player.id
    else:
        this_player = player.filter(id=player_id)[0]

    if not active_game:  # если активной игры нет
        # т.к. активной игры нет, то для автора последней активной игры нужно вывести сообщение
        # проверяем, что у автора есть game_id в сессии и он является автором is_creator
        # this_game_attempts - со скольки попыток угадали его число
        if game_id:
            this_game = game.filter(id=game_id)[0]
            this_creator = player_game_info.filter(player=this_player, game=this_game)[0].is_creator
            this_game_attempts = player_game_info.filter(game=this_game).order_by('-attempts')[0].attempts
            if this_creator:
                number_msg = f'Загаданное число: {this_game.guessed_number}'
                main_msg = f'Ваше число отгадали с {this_game_attempts} попытки'

        # т.к. активной игры нет, можно создать нову, поэтому выводим форму для загадывания числа
        # при отправке формы создается новая игра в бд и сохраняется в переменную this_game
        # также создается новая связь PlayerGameInfo, где указывается что этот игрок - автор
        # автору игры выводится сообщение
        if request.method == 'POST':
            form = MakeNumber(request.POST)
            this_game = form.save(commit=False)
            this_game.active = True
            this_game.save()
            request.session['game_id'] = this_game.id
            PlayerGameInfo.objects.create(player=this_player, game=this_game, is_creator=True, attempts=0)
            form = None
            number_msg = f'Загаданное число: {this_game.guessed_number}'
            info_msg = 'Второй игрок будет пытаться отгадать его'
        else:
            form = MakeNumber()

    else:  # если в данный момент уже идет игра

        # если в сессии нет game_id, сохраняем id активной игры
        # в переменную this_game сохраняем активную игру для дальнейшей работу
        if not game_id:
            request.session['game_id'] = active_game.id
            this_game = active_game
        else:
            if game_id != active_game.id:
                request.session['game_id'] = active_game.id
                this_game = active_game
            else:
                this_game = game.filter(id=game_id)[0]

        # проверяем есть ли связь между текущим игроком и текущей игрой, если есть проверяем авторство
        # связь сохраняем в переменную this_playergameinfo, авторство - в this_creator, для дальнейшей работы
        this_playergameinfo = player_game_info.filter(player=this_player, game=this_game)
        if len(this_playergameinfo) > 0:
            this_creator = this_playergameinfo[0].is_creator
        else:
            this_creator = False

        # т.к. игра уже идет, то выводим форму для угадыванния числа
        if request.method == 'POST':
            form = CheckNumber(request.POST)
            if form.is_valid():

                # если связь игра-игрок уже есть, то добавляем попытку, если нет - добавляем связь с одной попыткой
                if len(this_playergameinfo) > 0:
                    this_playergameinfo[0].attempts += 1
                    this_playergameinfo[0].save()
                else:
                    PlayerGameInfo.objects.create(player=this_player, game=this_game, is_creator=False, attempts=1)

                # выводим сообщение, после проверки предложенного числа
                entered_number = form.cleaned_data.get('number')
                if entered_number > active_game.guessed_number:
                    main_msg = f'Загаданное число меньше, чем {entered_number}'
                    form = CheckNumber()
                elif entered_number < active_game.guessed_number:
                    main_msg = f'Загаданное число больше, чем {entered_number}'
                    form = CheckNumber()
                else:
                    main_msg = 'Вы угадали число!'

                    # если число угадано, выводим форму для создания новой игры и дезактивируем текущую игру
                    form = MakeNumber()
                    active_game.active = False
                    active_game.save()
        else:
            if this_creator:  # если игра активна, то автору выводим сообщение
                number_msg = f'Загаданное число: {this_game.guessed_number}'
                main_msg = 'Ваше число еще не отгадали'
                form = None
            else:
                form = CheckNumber()

    context = {
        'form': form,
        'number_msg': number_msg,
        'info_msg': info_msg,
        'main_msg': main_msg
    }
    return render(
        request,
        'home.html',
        context
    )
