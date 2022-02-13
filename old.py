from flask import Flask, url_for, request, redirect
import os
app = Flask(__name__)
levels = {}


@app.route('/')
def page():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return 'И на Марсе будут яблони цвести!'


@app.route('/promotion_image')
def promotion_image():
    lst = [
        'Человечество вырастает из детства.',
        'Человечеству мала одна планета.',
        'Мы сделаем обитаемыми безжизненные пока планеты.',
        'И начнем с Марса!',
        'Присоединяйся!'
    ]
    url_pic = url_for('static', filename='img/mars.jpg')
    url_style = url_for('static', filename='styles/style3.css')
    return '''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet" 
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                        crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{}" />
                        <title>Колонизация</title>
                      </head>
                      <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="{}" alt="здесь должна была быть картинка, но не нашлась">
                        <div class="alert-dark" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-success" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-secondary" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-warning" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-danger" role="alert">
                          <br><h3>{}</h3>
                        </div>
                      </body>
                    </html>'''.format(url_style, url_pic, *lst)


@app.route('/promotion')
def promotion():
    lst = [
        'Человечество вырастает из детства.',
        'Человечеству мала одна планета.',
        'Мы сделаем обитаемыми безжизненные пока планеты.',
        'И начнем с Марса!',
        'Присоединяйся!'
    ]
    url_style = url_for('static', filename='styles/style3.css')
    return '''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet" 
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                        crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{}" />
                        <title>Колонизация</title>
                      </head>
                      <body>
                        <h1>Жди нас, Марс!</h1>
                        <div class="alert-dark" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-success" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-secondary" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-warning" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-danger" role="alert">
                          <br><h3>{}</h3>
                        </div>
                      </body>
                    </html>'''.format(url_style, *lst)


@app.route('/choice/<planet>')
def choice(planet):
    d = {
    "Меркурий": [
        'Первая планета от солнца;',
        'Самая маленькая в солнечной системы;',
        'Имеет разрушительную атмосферу;',
        'Есть гипотеза, что внешние слои планеты',
        'были сорваны в результате',
        'гигантского столкновения!'
    ],
    "Венера": [
        'Планета после Меркурия;',
        'Имеет толстую силикатную оболочку вокруг железного ядра;',
        'Имеет атмосферу;',
        'Называют сестрой Земли',
        'Самая горячая планета!'
    ],
    'Земля': [
        'Мы на ней живем (пока что);',
        'Самая пригодная для жизни;',
        'Третья от Солнца;',
        'Имеет атмосферу и гигантское;',
        'Количество воды!'
    ],
    "Марс": [
        'На ней много необходимых ресурсов;',
        'На ней есть вода и атмосфера;',
        'На ней есть небольшое магнитное поле;',
        'Очень популярна в SCI-FI!',
    ],
    "Юпитер": [
        'Самая большая планета;',
        'Газовый гигант, гравитация огромная;',
        'Меняет траекторию летящих мимо;',
        'Космических тел, защищая планеты;',
        'Имеет 79 спутников!'
    ],
    "Сатурн": [
        'Имеет несколько схожие с Юпитером',
        'Структуру атмосферы и магнитосферы;',
        'Планета известна обширной системой колец;',
        'Имеет 82 подтверждённых спутника, а 2 из',
        'Них проявляют признаки геологической активности,',
        'Про это есть серия в смешариках!'
    ],
    "Уран": [
        "Самая лёгкая планета среди гигантов;",
        "Плоскость экватора Урана наклонена к",
        "Плоскости его орбиты примерно на 98°,",
        "То есть планета лежит на боку!"
    ],
    "Нептун": [
        "Дальше всего от солнца;",
        "Спутник Тритон имеет гейзеры,",
        "Выпускающие жидкий азот;",
        "Также он, в отличие от других 13 спутников,",
        "Движется в другую сторону!"
    ],
    "Плутон": [
        "А всё, это уже не планета!"
    ]
    }
    if planet in d.keys():
        lst = d[planet]
    else:
        lst = d["Марс"]
    lst += [''] * (6 - len(lst))
    url_style = url_for('static', filename='styles/style3.css')
    return '''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet" 
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                        crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{}" />
                        <title>Колонизация</title>
                      </head>
                      <body>
                        <h1>Мое предложение: {}</h1>
                        <div class="alert-dark" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-success" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-secondary" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-warning" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-danger" role="alert">
                          <br><h3>{}</h3>
                        </div>
                        <div class="alert-bright" role="alert">
                          <br><h3>{}</h3>
                        </div>
                      </body>
                    </html>'''.format(url_style, planet, *lst)


@app.route('/image_mars')
def image():
    return """<!doctype html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <title>Привет, Марс!</title>
                    </head>
                    <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="{}" alt="здесь должна была быть картинка, но не нашлась">
                        <p>Вот она какая, красная планета.</p>
                    </body>
                </html>""".format(url_for('static', filename='img/mars.jpg'))


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def form_sample():
    url_style = url_for('static', filename='styles/style3.css')
    if request.method == 'GET':
        return '''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                             href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                             integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
                             crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{}"/>
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Анкета претендента</h1>
                            <h2>на участие в миссии</h2>
                            <div>
                                <form class="login_form" method="post">
                                    <div class="form-group">
                                      <input type="text" class="form-control" id="surname" placeholder="Введите фамилию" name="surname">
                                      <input type="text" class="form-control" id="name" placeholder="Введите имя" name="name">
                                    </div>
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <div class="form-group">
                                        <label for="educationSelect">Какое у Вас образование?</label>
                                        <select class="form-control" id="educationSelect" name="education">
                                          <option>Дошкольное</option>
                                          <option>Начальное</option>
                                          <option>Основное общее</option>
                                          <option>Среднее (полное)</option>
                                          <option>Среднее профессиональное</option>
                                          <option>Высшее профессиональное</option>
                                          <option>Бакалавриат</option>
                                          <option>Магистратура</option>
                                          <option>Аспирантура</option>
                                          <option>Докторантура</option>
                                        </select>
                                    </div>
                                    <div class="form-group form-check">
                                        <label for="profession">Какие у Вас есть професии?</label>
                                        <div><input type="checkbox" class="form-check-input" id="profession1" name="profession1">
                                        <label class="form-check-label" for="profession1">Инженер-исследователь</label></div>
                                        <div><input type="checkbox" class="form-check-input" id="profession2" name="profession2">
                                        <label class="form-check-label" for="profession2">Инженер-строитель</label></div>
                                        <div><input type="checkbox" class="form-check-input" id="profession3" name="profession3">
                                        <label class="form-check-label" for="profession3">Пилот</label></div>
                                        <div><input type="checkbox" class="form-check-input" id="profession4" name="profession4">
                                        <label class="form-check-label" for="profession4">Метеоролог</label></div>
                                        <div><input type="checkbox" class="form-check-input" id="profession5" name="profession5">
                                        <label class="form-check-label" for="profession5">Инженер по жизнеобеспечению</label></div>
                                        <div><input type="checkbox" class="form-check-input" id="profession6" name="profession6">
                                        <label class="form-check-label" for="profession6">Инженер по радиационной защите</label></div>
                                        <div><input type="checkbox" class="form-check-input" id="profession7" name="profession7">
                                        <label class="form-check-label" for="profession7">Врач</label></div>
                                        <div><input type="checkbox" class="form-check-input" id="profession8" name="profession8">
                                        <label class="form-check-label" for="profession8">Экзобиолог</label></div>
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="about">Почему вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="reason" rows="3" placeholder="В КОДЕ ЭЛЕМЕНТА УБЕРИТЕ ПЕРЕВОД СТРОКИ В CSS И ВСЕ ЗАРАБОТАЕТ" name="reason"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готовы остаться на Марсе?</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''.format(url_style)
    elif request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        email = request.form['email']
        education = request.form['education']
        educations = ['Дошкольное', 'Начальное', 'Основное общее', 'Среднее (полное)',
                      'Среднее профессиональное', 'Высшее профессиональное', 'Бакалавриат',
                      'Магистратура', 'Аспирантура', 'Докторантура']
        professions = [request.form['profession' + str(i)] for i in range(1, 9) if 'profession' + str(i) in list(request.form)]
        sex = request.form['sex']
        motivation = request.form['reason']
        file = request.form['file']
        nickname = surname + "+" + name
        score = (len(professions) * 10 + len(motivation)) / 4 + educations.index(education) * 5.5
        if nickname in levels.keys():
            levels[nickname]["level"] += 1
            levels[nickname]["score"] = score
        else:
            levels[nickname] = {"level": 1, "score": score}
        return redirect('/results/{}/{}/{}'.format(nickname, levels[nickname]["level"], levels[nickname]["score"]))


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def result(nickname, level, rating):
    url_style = url_for('static', filename='styles/style3.css')
    return '''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet" 
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                        crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{}" />
                        <title>Результаты</title>
                      </head>
                      <body>
                        <h1>Результаты отбора</h1>
                        <h2>Претендента на участии {}:</h2>
                        <div class="alert-success" role="alert">
                          <br><h3>Поздравляем! Ваш рейтинг после {} этапа отбора</h3>
                        </div>
                        <div class="alert-bright" role="alert">
                          <br><h3>составляет {}</h3>
                        </div>
                        <div class="alert-warning" role="alert">
                          <br><h3>Желаем удачи!</h3>
                        </div>
                      </body>
                    </html>'''.format(url_style, nickname, level, rating)


@app.route('/load_photo', methods=['POST', 'GET'])
def load_photo():
    url_style = url_for('static', filename='styles/style3.css')
    image = url_for('static', filename='img/img.png')
    if request.method == 'GET':
        return '''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                             href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                             integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
                             crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{}"/>
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1>Загрузка фотографии</h1>
                            <h2>для участия в миссии</h2>
                            <div>
                                <form class="login_form" method="post" enctype="multipart/form-data">
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию и нажмите Shift+F5</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                        <image src={} alt="no upload">
                                    </div>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''.format(url_style, image)
    elif request.method == 'POST':
        f = request.files['file']
        path = os.path.abspath(os.getcwd()) + '\\static\\img\\img.png'
        if os.path.exists(path):
            os.remove(path)
        f.save(path)
        return redirect('/load_photo')


@app.route('/carousel')
def carousel():
    url_style = url_for('static', filename='styles/style3.css')
    lst = [url_for('static', filename='img/galery/carousel1.jpg'),
           url_for('static', filename='img/galery/carousel2.jpg'),
           url_for('static', filename='img/galery/carousel3.jpg')]
    return '''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet" 
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                        crossorigin="anonymous">
                        <title>Пейзажи Марса</title>
                      </head>
                      <body>
                        <h1>Пейзажи марса</h1>
                        <div id="carouselExampleControls" class="carousel" data-slide="carousel">
                          <div class="carousel-inner">
                            <div class="carousel-item active">
                              <img class="d-block w-100" src="{}" alt="First slide">
                            </div>
                            <div class="carousel-item">
                              <img class="d-block w-100" src="{}" alt="Second slide">
                            </div>
                            <div class="carousel-item">
                              <img class="d-block w-100" src="{}" alt="Third slide">
                            </div>
                          </div>
                          <div>
                          <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="sr-only">Previous</span>
                          </a>
                          <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="sr-only">Next</span>
                          </a>
                        </div>
                      </body>
                    </html>'''.format(*lst)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')