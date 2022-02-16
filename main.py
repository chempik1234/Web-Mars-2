from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from random import randint
import os
import json
from data import db_session
from data.__all_models import *
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
        professions = [all_profs[i - 1] for i in range(1, 9) if
                       'profession' + str(i) in list(request.form)]
        with open(PATH + '\\templates\\accounts.json', 'r') as cat_file:
            readd = cat_file.read()
            data = json.loads(readd)
            id = len(data)
        with open(PATH + '\\templates\\accounts.json', 'w') as cat_file:
            if len(readd) > 2:
                cat_file.write(readd[: -1] + ',\n' + json.dumps({'name': request.form['name'],
                                                                          'surname': request.form['surname'],
                                                                          'file': request.form['name'],
                                                                          'professions': professions,
                                                                          'id': id}, ensure_ascii=False) + ']')
            else:
                cat_file.write('[' + json.dumps({'name': request.form['name'],
                                                                          'surname': request.form['surname'],
                                                                          'file': request.form['name'],
                                                                          'professions': professions,
                                                                          'id': id}, ensure_ascii=False) + ']')
        if 'file' in request.files.keys():
            f = request.files['file']
            if f.filename:
                path = PATH + f'\\static\\img\\avatars\\img{id + 1}.png'
                f.save(path)
        professions = '\n'.join(professions)
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
    return render_template('login.html', style=url_style,
                           header='<h2><span class="i"></span>Аварийный доступ</h2>',
                           title='Авторизация', form=form)


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
    global PATH
    PATH2 = PATH + '\\static\\img\\galery\\'
    url_style = url_for('static', filename='styles/style3.css')
    photos = [url_for('static', filename='img/galery/' + f) for f in os.listdir(PATH2) if os.path.isfile(os.path.join(PATH2, f))]
    if request.method == 'GET':
        return render_template('carousel_with_load.html', style=url_style,
                               photos=photos)
    elif request.method == 'POST':
        f = request.files['file']
        path = PATH2 + f'img{len(photos)}.png'
        if os.path.exists(path):
            os.remove(path)
        f.save(path)
        return redirect('/galery')


@app.route('/member')
def random_member():
    with open(PATH + '\\templates\\accounts.json', 'r') as cat_file:
        readd = cat_file.read()
        data = json.loads(readd)
        id = randint(1, len(data))
    style = url_for('static', filename='/styles/style3.css')
    return render_template('random_user.html', style=style,
                           title='Случайная страница',
                           params=data, id=id)


@app.route('/works')
@app.route('/')
def works_list():
    d = []
    headers = ['Title of activity', 'Team leader',
               'Duration', 'List of collaborators',
               'Is finished']
    for job in db_sess.query(Jobs).all():
        d.append({i: None for i in headers})
        d[-1][headers[0]] = job.job
        cap = db_sess.query(User).filter(User.id == job.team_leader).first()
        d[-1][headers[1]] = cap.surname + ' ' + cap.name
        d[-1][headers[2]] = str(job.work_size) + ' hours'
        d[-1][headers[3]] = job.collaborators
        if job.is_finished:
            d[-1][headers[4]] = 'Is finished'
        else:
            d[-1][headers[4]] = 'Is not finished'
    style = url_for('static', filename='/styles/style3.css')
    return render_template('works_list.html', style=style, title='Журнал работ',
                           dictionary=d, keys=headers)


class DBLoginForm(FlaskForm):
    surname = StringField("Surname", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    speciality = StringField("Speciality", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    email = StringField("Login / Email", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password',
                                    validators=[DataRequired(),
                                                EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Войти')


@app.route('/register', methods=['GET','POST'])
def register():
    form = DBLoginForm()
    url_style = url_for('static', filename='styles/style3.css')
    if form.validate_on_submit():
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.hashed_password = form.password.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/success')
    return render_template('login.html', style=url_style,
                           header='<h2>Register form</h2>',
                           title='Авторизация', form=form)


def db_main():
    people_amount = 6
    ##### ADD PERSONAL
    surnames = ["Scott", "Jackson", "Kamado", "Carry", "Brown", "Freeman"]
    names = ["Riddley", "Michael", "Manfred", "Ben", "John", "Albert"]
    ages = [21, 23, 34, 29, 38, 25]
    positions = ["captain", "private", "corporal", "private first class", "staff-sergeant", "private"]
    specialities = ["research engineer", "research engineer", "life support engineer",
                    "drone pilot", "medic", "builder"]
    addresses = ["module_1", "module_1", "module_2", "module_3", "module_2", "module_3"]
    emails = ["scott_chief@mars.org", "michael_singer@mars.org", "foreigner_guy@mars.org",
              "arma_III@mars.org", "stereotypical_name@mars.org", "science4life@mars.org"]
    for i in range(people_amount):
        user = User()
        user.surname = surnames[i]
        user.name = names[i]
        user.age = ages[i]
        user.position = positions[i]
        user.speciality = specialities[i]
        user.address = addresses[i]
        user.email = emails[i]
        db_sess.add(user)
    ##### ADD JOB
    leaders = [1, 3, 4]
    jobs = ["Deployment of residential modules 1 and 2",
            "Exploration of mineral resources",
            "Development of a management system"]
    work_sizes = [15, 15, 25]
    collaborators_lists = ["1, 3", "4, 3", "5"]
    finished_list = [False, False, False]
    jobs_amount = 3
    for i in range(jobs_amount):
        job = Jobs()
        job.team_leader = leaders[i]
        job.job = jobs[i]
        job.work_size = work_sizes[i]
        job.collaborators = collaborators_lists[i]
        #job.data is default (now)
        job.is_finished = finished_list[i]
        db_sess.add(job)
    db_sess.commit()


if __name__ == '__main__':
    PATH = os.path.abspath(os.getcwd())
    needtofill = os.path.isfile(PATH + '\\db\\mars_explorer.db')
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    if not needtofill:
        db_main()
    app.run(port=8080, host='127.0.0.1')