from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from random import randint
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
levels = {}


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    url_style = url_for('static', filename='styles/style3.css')
    return render_template('base.html', title=title, style=url_style)


@app.route('/training/<prof>')
def training(prof):
    if "инженер" in prof or "строитель" in prof:
        img = "engineer.jpg"
        simulator = "Инженерный центр"
    else:
        img = "science.jpg"
        simulator = "Научные симуляторы"
    url_style = url_for('static', filename='styles/style3.css')
    return render_template('training.html', title="Подбор центра", simulator=simulator,
                           profession=url_for('static', filename='img/' + img), style=url_style)


@app.route('/list_prof/<list>')
def list_prof(list):
    url_style = url_for('static', filename='styles/style3.css')
    professions = ['Инженер-исследователь', 'Инженер-строитель',
                   'Пилот', 'Метеоролог', 'Инженер по жизнеобеспечению',
                   'Инженер по радиационной защите', 'Врач',
                   'Экзобиолог']
    if list != 'ol' and list != 'ul':
        return 'Wrong parameter: ' + str(list) + '. It must be "ol" or "ul"'
    return render_template('list_prof.html', title="Список профессий",
                           list=list, professions=professions, style=url_style)


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def form_sample():
    url_style = url_for('static', filename='styles/style3.css')
    if request.method == 'GET':
        return render_template('form_login.html', style=url_style)
    elif request.method == 'POST':
        redirect('/answer')
        all_profs = ['Инженер-исследователь', 'Инженер-строитель',
                    'Пилот', 'Метеоролог', 'Инженер по жизнеобеспечению',
                    'Инженер по радиационной защите', 'Врач',
                    'Экзобиолог']
        professions = '\n'.join([all_profs[i - 1] for i in range(1, 9) if
                                 'profession' + str(i) in list(request.form)])
        if 'accept' in request.form:
            acc = "True"
        else:
            acc = "False"
        return redirect(url_for('answer', surname=request.form['surname'],
                                name=request.form['name'],
                                education=request.form['education'],
                                professions=professions,
                                sex=request.form['sex'],
                                reson=request.form['reason'],
                                accept=acc,
                                style=url_style))


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    if not request.args.get('surname'):
        return 'MUST BE REDIRECTED FROM THE LOGIN FORM'
    #form = form[20: -2]
    url_style = url_for('static', filename='styles/style3.css')
    return render_template('auto_answer.html', title="Анкета",
                           surname=request.args.get('surname'),
                           name=request.args.get('name'),
                           education=request.args.get('education'),
                           professions=request.args.get('professions').split('\n'),
                           sex=request.args.get('sex'),
                           reson=request.args.get('reason'),
                           accept=request.args.get('accept'),
                           style=url_style)


class LoginForm(FlaskForm):
    id = StringField('Id астронавта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    cap_id = StringField('Id капитана', validators=[DataRequired()])
    cap_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    url_style = url_for('static', filename='styles/style3.css')
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', style=url_style, title='Авторизация', form=form)


@app.route('/distribution')
def distribution():
    url_style = url_for('static', filename='styles/style3.css')
    lst = request.args.get('people')
    if lst is None:
        return 'NO PEOPLE'
    return render_template('distribution.html', style=url_style, people=lst.split(','))


@app.route('/table/<string:sex>/<int:age>')
def table(sex, age):
    url_style = url_for('static', filename='styles/style3.css')
    hex = '0123456789ABCDEF'
    if sex == "female":
        color = '#' + hex[randint(7, 15)] * 2 + hex[randint(3, 6)] * 2 + '00'
    else:
        color = '#' + '00' + hex[randint(4, 6)] * 2 + hex[randint(7, 15)] * 2
    if age < 21:
        image = url_for('static', filename="img/decoration_kid.png")
    else:
        image = url_for('static', filename="img/decoration_adult.png")
    return render_template('table.html', style=url_style, color=color, image=image)


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    PATH = os.path.abspath(os.getcwd()) + '\\static\\img\\galery\\'
    url_style = url_for('static', filename='styles/style3.css')
    photos = [url_for('static', filename='img/galery/' + f) for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
    print(photos)
    if request.method == 'GET':
        return render_template('carousel_with_load.html', style=url_style,
                               photos=photos)
    elif request.method == 'POST':
        f = request.files['file']
        path = PATH + f'img{len(photos)}.png'
        if os.path.exists(path):
            os.remove(path)
        f.save(path)
        return redirect('/galery')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')