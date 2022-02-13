from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    if "инженер" in prof or "строитель" in prof:
        img = "engineer.jpg"
        simulator = "Инженерный центр"
    else:
        img = "science.jpg"
        simulator = "Научные симуляторы"
    return render_template('training.html', title="Подбор центра", simulator=simulator,
                           profession=url_for('static', filename='img/' + img))


@app.route('/list_prof/<list>')
def list_prof(list):
    professions = ['Инженер-исследователь', 'Инженер-строитель',
                   'Пилот', 'Метеоролог', 'Инженер по жизнеобеспечению',
                   'Инженер по радиационной защите', 'Врач',
                   'Экзобиолог']
    return render_template('list_prof.html', title="Список профессий",
                           list=list, professions=professions)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')