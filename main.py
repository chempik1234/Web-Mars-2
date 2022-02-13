from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)
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
        return answer(request.form)


@app.route('/answer')
@app.route('/auto_answer')
def answer(form=None):
    if not form:
        return 'MUST BE REDIRECTED FROM THE LOGIN FORM'
    url_style = url_for('static', filename='styles/style3.css')
    all_profs = ['Инженер-исследователь', 'Инженер-строитель',
                 'Пилот', 'Метеоролог', 'Инженер по жизнеобеспечению',
                 'Инженер по радиационной защите', 'Врач',
                 'Экзобиолог']
    professions = [all_profs[i - 1] for i in range(1, 9) if
                   'profession' + str(i) in list(form)]
    if form['accept']:
        acc = "True"
    else:
        acc = "False"
    return render_template('auto_answer.html', title="Анкета",
                           surname=form['surname'],
                           name=form['name'],
                           education=form['education'],
                           professions=professions,
                           sex=form['sex'],
                           reson=form['reason'],
                           accept=acc,
                           style=url_style)



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')