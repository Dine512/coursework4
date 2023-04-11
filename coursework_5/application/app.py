

from flask import Flask, render_template, request, redirect, session
from unit import PlayerUnit, EnemyUnit
from base import Arena
from classes import unit_classes
from equipment import Equipment
app = Flask(__name__, template_folder="../templates")
app.config["SECRET_KEY"] = "1231241"
heroes = {}
session_dict = {}
log = []

sessions_count = 0
@app.route("/")
def menu_page():
    # TODO рендерим главное меню (шаблон index.html)
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)
    session_id = session.get('session_id')
    session_dict[session_id]['arena'] = arena = Arena()
    session_dict[session_id]['log'] = []
    arena.start_game(session_dict[session_id]['player'], session_dict[session_id]['enemy'])
    return render_template('fight.html', heroes=session_dict[session_id])

@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    session_id = session.get('session_id')
    _session = session_dict[session_id]
    arena = _session['arena']
    if not arena.game_is_running:
        return render_template('fight.html', heroes=_session, log=_session['log'])

    _session["log"].append(arena.player_hit())
    _session["log"].append(arena.next_turn())
    return render_template('fight.html', heroes=_session, log=_session['log'])


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    session_id = session.get('session_id')
    _session = session_dict[session_id]
    arena = _session['arena']
    if not arena.game_is_running:
        return render_template('fight.html', heroes=_session, log=_session['log'])
    _session["log"].append(arena.player_use_skill())
    _session["log"].append(arena.next_turn())
    return render_template('fight.html', heroes=_session, log=_session['log'])


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    session_id = session.get('session_id')
    _session = session_dict[session_id]
    arena = _session['arena']

    _session["log"].append(arena.next_turn())
    return render_template('fight.html', heroes=_session, log=_session['log'])



@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    session_id = session.get('session_id')
    session_dict.pop(session_id)

    return redirect("/")


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    global sessions_count
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

        # heroes['player'] = PlayerUnit(name=name, unit_class=unit_class, weapon=weapon, armor=armor)

        sessions_count += 1
        session["session_id"] = sessions_count
        session_dict[sessions_count] = {"player": PlayerUnit(name=name, unit_class=unit_class, weapon=weapon, armor=armor)}
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

        # heroes['enemy'] = EnemyUnit(name=name, unit_class=unit_class, weapon=weapon, armor=armor)
        if 'session_id' in session:
            session_id = session.get('session_id')
            session_dict[session_id]['enemy'] = EnemyUnit(name=name, unit_class=unit_class, weapon=weapon, armor=armor)
        return redirect("/fight/")


if __name__ == "__main__":
    app.run()
