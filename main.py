import flask
from flask import Flask, render_template, url_for, redirect, request, abort, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, EqualTo
from random import randint
import os
import json
from data import db_session
from data.__all_models import *
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash
from data.category import *
from data.api import blueprint
from data.reqparse_user import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy_serializer import *
import requests
from flask_restful import reqparse, abort, Api, Resource
app = Flask(__name__)
api = Api(app)
api.add_resource(UserListResource, '/api/v2/users')
api.add_resource(UserListResource, '/api/v2/users/<int:user_id>')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
levels = {}


@app.errorhandler(404)
def not_found(error):
    return make_response(flask.jsonify({'error': '404'}), 404)


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


@app.route('/login_old', methods=['GET', 'POST'])
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
               'Hazard category', 'Is finished']
    for job in db_sess.query(Jobs).all():
        d.append({i: None for i in headers})
        d[-1][headers[0]] = job.job
        cap = db_sess.query(User).filter(User.id == job.team_leader).first()
        d[-1][headers[1]] = cap.surname + ' ' + cap.name
        d[-1][headers[2]] = str(job.work_size) + ' hours'
        d[-1][headers[3]] = job.collaborators
        category = db_sess.query(Category).filter(job.category == Category.id).first()
        if category:
            d[-1][headers[4]] = category.name
        else:
            d[-1][headers[4]] = 'NO CATEGORY'
        if job.is_finished:
            d[-1][headers[5]] = 'Is finished'
        else:
            d[-1][headers[5]] = 'Is not finished'
        d[-1]["team_leader"] = job.team_leader
        d[-1]["id"] = job.id
    style = url_for('static', filename='/styles/style3.css')
    return render_template('works_list.html', style=style, title='Журнал работ',
                           dictionary=d, keys=headers)


@app.route('/departments')
def departments_list():
    d = []
    headers = ['Title of department', 'Chief',
               'Members', 'Department email']
    for dep in db_sess.query(Department).all():
        d.append({i: None for i in headers})
        d[-1][headers[0]] = dep.title
        cap = db_sess.query(User).filter(User.id == dep.chief).first()
        d[-1][headers[1]] = cap.surname + ' ' + cap.name
        d[-1][headers[2]] = dep.members
        d[-1][headers[3]] = dep.email
        d[-1]["chief"] = dep.chief
        d[-1]["id"] = dep.id
    style = url_for('static', filename='/styles/style3.css')
    return render_template('departments_list.html', style=style, title='Журнал отделений',
                           dictionary=d, keys=headers)


class DBLoginForm(FlaskForm):
    surname = StringField("Surname", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    speciality = StringField("Speciality", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    email = EmailField("Login / Email", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password',
                                    validators=[DataRequired(),
                                                EqualTo('password', message='Passwords must match')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class DBJobLoginForm(FlaskForm):
    team_leader = IntegerField("Team Leader ID", validators=[DataRequired()])
    job = StringField("Job", validators=[DataRequired()])
    work_size = IntegerField("Work size (hours per day)", validators=[DataRequired()])
    collaborators = StringField("Collaborators ID's (divide with comma)", validators=[DataRequired()])
    is_finished = BooleanField("Is finished?")
    submit = SubmitField('Отправить')


class DBDepLoginForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    chief = IntegerField("Chief", validators=[DataRequired()])
    members = StringField("Members", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField('Отправить')


class SignInForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
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

# jobs


@app.route('/add_job', methods=['GET','POST'])
def register_job():
    form = DBJobLoginForm()
    url_style = url_for('static', filename='styles/style3.css')
    if form.validate_on_submit():
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job_add.html', style=url_style,
                           header='<h2>Job registering form</h2>',
                           title='Добавление работы', form=form)


@app.route('/edit_job/<int:id_>', methods=['GET','POST'])
def edit_job(id_):
    form = DBJobLoginForm()
    url_style = url_for('static', filename='styles/style3.css')
    if current_user.is_authenticated:
        job = db_sess.query(Jobs).filter(Jobs.id == id_).first()
        author = job.team_leader
        if current_user.id != 1 and current_user.id != author:
            abort(403)
    else:
        abort(403)
    if request.method == "GET":
        job = db_sess.query(Jobs).filter(Jobs.id == id_).first()
        if job:
            form.job.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(403)
    if form.validate_on_submit():
        job = db_sess.query(Jobs).filter(Jobs.id == id_).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.add(job)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job_add.html', style=url_style,
                           header='<h2>Job editing form</h2>',
                           title='Изменение работы', form=form)


@app.route('/delete_job/<int:id_>')
def delete_job(id_):
    url_style = url_for('static', filename='styles/style3.css')
    if current_user.is_authenticated:
        job = db_sess.query(Jobs).filter(Jobs.id == id_).first()
        author = job.team_leader
        if current_user.id != 1 and current_user.id != author:
            abort(403)
    else:
        abort(403)
    job = db_sess.query(Jobs).filter(Jobs.id == id_).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
        return redirect('/')
    else:
        abort(404)
    return render_template('job_delete.html', style=url_style,
                           header='<h2>Job deleting form</h2>',
                           title='Удаление работы')

# departments


@app.route('/add_department', methods=['GET','POST'])
def register_department():
    form = DBDepLoginForm()
    url_style = url_for('static', filename='styles/style3.css')
    if form.validate_on_submit():
        dep = Department()
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/')
    return render_template('/dep_add.html', style=url_style,
                           header='<h2>Department registering form</h2>',
                           title='Добавление отделения', form=form)


@app.route('/edit_department/<int:id_>', methods=['GET','POST'])
def edit_department(id_):
    form = DBDepLoginForm()
    url_style = url_for('static', filename='styles/style3.css')
    if current_user.is_authenticated:
        dep = db_sess.query(Department).filter(Department.id == id_).first()
        author = dep.chief
        if current_user.id != 1 and current_user.id != author:
            abort(403)
    else:
        abort(403)
    if request.method == "GET":
        dep = db_sess.query(Department).filter(Department.id == id_).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(403)
    if form.validate_on_submit():
        dep = db_sess.query(Department).filter(Department.id == id_).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.add(dep)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('dep_add.html', style=url_style,
                           header='<h2>Department editing form</h2>',
                           title='Изменение отделения', form=form)


@app.route('/delete_department/<int:id_>')
def delete_department(id_):
    url_style = url_for('static', filename='styles/style3.css')
    if current_user.is_authenticated:
        dep = db_sess.query(Department).filter(Department.id == id_).first()
        author = dep.chief
        if current_user.id != 1 and current_user.id != author:
            abort(403)
    else:
        abort(403)
    dep = db_sess.query(Department).filter(Department.id == id_).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
        return redirect('/')
    else:
        abort(404)
    return render_template('dep_delete.html', style=url_style,
                           header='<h2>Department deleting form</h2>',
                           title='Удаление отделения')


def get_size(address):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {"apikey": api_key, "lang": "ru_RU", "text": address}
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    organization = json_response["features"][0]["properties"]
    toponym_lc, toponym_uc = organization["boundedBy"]
    toponym_size = max(abs(toponym_lc[0] - toponym_uc[0]),
                       abs(toponym_lc[1] - toponym_uc[1]))
    return str(toponym_size)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    if not db_sess.query(User).get(user_id):
        return flask.jsonify({'error': 'No such user'})
    url_style = url_for('static', filename='styles/style3.css')
    user = db_sess.query(User).get(user_id)
    surname, name = user.surname, user.name
    town = user.city_from
    image_src = None
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": town,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        map_params = {
            "ll": toponym_coodrinates.replace(' ', ','),
            "spn": ','.join([get_size(town) for _ in range(2)]),
            "l": "sat"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        if response:
            image_src = response.url
    return render_template('users_show.html', title='Hometown',
                           style=url_style, surname=surname,
                           name=name, town=town, image_src=image_src)


@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    url_style = url_for('static', filename='styles/style3.css')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/success")
        return render_template('sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('sign_in.html', title='Авторизация', form=form, style=url_style)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/success')
def success():
    return redirect('/')


def db_main():
    people_amount = 6
    # ADD PERSONAL
    surnames = ["Scott", "Jackson", "Kamado", "Carry", "Brown", "Freeman"]
    names = ["Riddley", "Michael", "Manfred", "Ben", "John", "Albert"]
    ages = [21, 23, 34, 29, 38, 25]
    positions = ["captain", "private", "corporal", "private first class", "staff-sergeant", "private"]
    specialities = ["research engineer", "research engineer", "life support engineer",
                    "drone pilot", "medic", "builder"]
    addresses = ["module_1", "module_1", "module_2", "module_3", "module_2", "module_3"]
    emails = ["scott_chief@mars.org", "michael_singer@mars.org", "foreigner_guy@mars.org",
              "arma_III@mars.org", "stereotypical_name@mars.org", "science4life@mars.org"]
    passwords = ['1', '2', '3', '4', '5', '6']
    cities = ['New York', 'Gary, Indiana', 'Tokyo', 'Rome', 'Cape Town', 'Oslo']
    for i in range(people_amount):
        user = User()
        user.surname = surnames[i]
        user.name = names[i]
        user.age = ages[i]
        user.position = positions[i]
        user.speciality = specialities[i]
        user.address = addresses[i]
        user.email = emails[i]
        user.hashed_password = passwords[i]
        user.city_from = cities[i]
        db_sess.add(user)
    # ADD JOB
    leaders = [1, 3, 4]
    jobs = ["Deployment of residential modules 1 and 2",
            "Exploration of mineral resources",
            "Development of a management system"]
    work_sizes = [15, 15, 25]
    collaborators_lists = ["1, 3", "4, 3", "5"]
    finished_list = [False, False, False]
    cats = ['1', '3', '2']
    jobs_amount = 3
    for i in range(jobs_amount):
        job = Jobs()
        job.team_leader = leaders[i]
        job.job = jobs[i]
        job.work_size = work_sizes[i]
        job.collaborators = collaborators_lists[i]
        # job.data is default (now)
        job.is_finished = finished_list[i]
        job.category = cats[i]
        db_sess.add(job)
    # ADD DEPARTMENTS
    titles = ["Department_1", "Department_2", "Deppppp_3", "dep4"]
    chiefs = [1, 1, 5, 5]
    members = ["1, 2, 3", "1, 4, 5", "4, 5", "2, 3, 5"]
    emails = ["dep1@mars.org", "dep2@mars.org", "depIII@mars.org", "dep4mars.org"]
    dep_amount = 4
    for i in range(dep_amount):
        dep = Department()
        dep.title = titles[i]
        dep.chief = chiefs[i]
        dep.members = members[i]
        dep.email = emails[i]
        db_sess.add(dep)
    # ADD CATEGORIES
    names = ['first', 'second', 'third']
    cat_amount = 3
    for i in range(cat_amount):
        cat = Category()
        cat.name = names[i]
        db_sess.add(cat)
    db_sess.commit()


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    app.register_blueprint(blueprint)
    PATH = os.path.abspath(os.getcwd())
    needtofill = os.path.isfile(PATH + '\\db\\mars_explorer.db')
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    if not needtofill:
        db_main()
    app.run(port=8080, host='127.0.0.1')