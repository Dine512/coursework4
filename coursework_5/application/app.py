

from flask import Flask, render_template, request, redirect
from unit import PlayerUnit, EnemyUnit
from base import Arena
from classes import unit_classes
from equipment import Equipment
app = Flask(__name__, template_folder="../templates")

heroes = {}

arena = Arena() # TODO инициализируем класс арены
log = []

@app.route("/")
def menu_page():
    # TODO рендерим главное меню (шаблон index.html)
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)
    arena.start_game(heroes['player'], heroes['enemy'])
    return render_template('fight.html', heroes=heroes)

@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    if not arena.game_is_running:
        return render_template('fight.html', heroes=heroes, log=log)

    log.append(arena.player_hit())
    log.append(arena.next_turn())
    return render_template('fight.html', heroes=heroes, log=log)


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    if not arena.game_is_running:
        return render_template('fight.html', heroes=heroes, log=log)
    log.append(arena.player_use_skill())
    log.append(arena.next_turn())
    return render_template('fight.html', heroes=heroes, log=log)


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    log.append(arena.next_turn())
    return render_template('fight.html', heroes=heroes, log=log)



@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    global log
    arena._end_game()
    log = []

    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == 'GET':
        equipment = {"weapon_list": Equipment().get_weapons_names(),
                     "armor_list": Equipment().get_armors_names()}
        return render_template('hero_choosing.html', unit_classes=unit_classes, equipment=equipment, header='Выберите героя')

    if request.method == "POST":
        name = request.form.get('name')

        unit_class = request.form.get('unit_class')
        unit_class = unit_classes.get(unit_class)

        weapon = request.form.get('weapon')
        weapon = Equipment().get_weapon(weapon)

        armor = request.form.get('armor')
        armor = Equipment().get_armor(armor)

        heroes['player'] = PlayerUnit(name=name, unit_class=unit_class, weapon=weapon, armor=armor)
        return redirect("/choose-enemy/")
    # TODO кнопка выбор героя. 2 метода GET и POST
    # TODO на GET отрисовываем форму.
    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    pass


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == 'GET':
        equipment = {"weapon_list": Equipment().get_weapons_names(),
                     "armor_list": Equipment().get_armors_names()}
        return render_template('hero_choosing.html', unit_classes=unit_classes, equipment=equipment, header='Выберите противника')

    if request.method == "POST":
        name = request.form.get('name')

        unit_class = request.form.get('unit_class')
        unit_class = unit_classes.get(unit_class)

        weapon = request.form.get('weapon')
        weapon = Equipment().get_weapon(weapon)

        armor = request.form.get('armor')
        armor = Equipment().get_armor(armor)

        heroes['enemy'] = EnemyUnit(name=name, unit_class=unit_class, weapon=weapon, armor=armor)
        return redirect("/fight/")


if __name__ == "__main__":
    app.run()
