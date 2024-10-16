from flask import Flask, request, make_response, abort,  url_for, redirect, render_template
from aplicacion.forms import formcalculadora,UploadForm
from werkzeug.utils import secure_filename
from os import listdir
from flask_bootstrap import Bootstrap5



app = Flask(__name__)
bootstrap = Bootstrap5(app)


# @app.route('/')
# def hello_world():
#     return 'Hola'

@app.route("/hello/")
@app.route("/hello/<string:nombre>")
@app.route("/hello/<string:nombre>/<int:edad>")
def hola(nombre = None, edad =  None):
    if nombre and edad:
        return 'Hola, {0} tienes {1} años.'.format(nombre, edad)
    elif nombre:
        return 'Hola, {0}'.format(nombre)
    else:
        return 'Hola mundo'


@app.route('/articulos/')
def articulos():
    return 'Lista de artículos'


@app.route('/articulos/<id>')
def mostrar_articulos(id):
    return 'Vamos a mostrar el artículo con id:{}'.format(id)

@app.route('/articulos/new', methods = ["POST"])
def articulos_new():
    return 'Está URL recibe información de un formulario con el método POST'

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Hemos accedido con POST'
    else:
        return 'Hemos accedido con GET'

@app.route('/acercade')
def acercade():
    return 'Página acerca de ...'

@app.route("/suma", methods = ["GET", "POST"])
def sumar():
    if request.method == "POST":
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")
        return str(int(num1) + int(num2))
    else:
        return '''<form action = "/suma" method = "POST">
        <label>N1:</label>
        <input type = "text" name = "num1"/>
        <label>N2:</label>
        <input type = "text" name = "num2"/>
        <input type = "submit"/>
        </form>'''  
    

@app.route('/object/')
def return_object():
    headers = {'Content-Type' : 'text/plain'}
    return make_response('Hello, World!', 200, headers)

@app.route('/tuple/')
def return_tuple():
    return 'Hello, World! - tuple', 200, {'Content-Type' : 'text/plain'}

@app.route('/login2/')
def return_login2():
    abort(401)

# @app.errorhandler(404)
# def page_not_found(error):
#     return 'Página no encontrada...', 404

""""@app.route('/')"""

@app.route('/string/')
def return_string():
    return 'Hello, World!'

# @app.route('/')
# def index():
#     return redirect(url_for('return_string'))

# @app.route('/')
# def inicio():
#     return '<img src = "' + url_for('static', filename = 'img/tux.png') + '"/>'


# ULTIMO EJERCICIO CON LA CALCULADORA Y BOOTSTRAP

# @app.route('/')
# def inicio():
#     return render_template("inicio.html")

# @app.route('/hola1')
# @app.route('/hola1/<nombre>/')
# def saluda(nombre = None):
#     return render_template("template1.html", nombre=nombre)


# @app.route('/suma/<num1>/<num2>')
# def suma(num1, num2):
#     try:
#         resultado =  int(num1) + int(num2)
#     except:
#         abort(404)
#     return render_template("template2.html", num1 =  num1, num2 = num2, resultado = resultado)

# @app.route('/tabla/<numero>')
# def tabla(numero):
#     try:
#         numero = int(numero)
#     except:
#         abort(404)
#     return render_template("template3.html", num = numero)

# Texto aleatorio para token de CSRF
app.secret_key ='texto aleatorio adlakjsfñaksd'

# @app.route('/')
# def inicio():
#     return render_template("inicio.html")

@app.route("/calculadora_post", methods=["get", "post"])
def calculadora_post():
    if request.method=="POST":
        num1=request.form.get("num1")
        num2=request.form.get("num2")
        operador=request.form.get("operador")

        try:
            resultado=eval(num1+operador+num2)
        except:
            return render_template("error.html", error="No puedo realizar la operación")
        return render_template("resultado.html", num1=num1, num2=num2, operador=operador, resultado= resultado)
    else:
        return render_template("calculadora_post.html")

@app.route("/calculadora_post_wtf", methods=["get", "post"])
def calculadora_post_wtf():
    form=formcalculadora(request.form)
    if form.validate_on_submit():
        num1=form.num1.data
        num2=form.num2.data
        operador=form.operador.data
        try:
            resultado=eval(str(num1)+operador+str(num2))
        except:
            return render_template("error.html", error="No puedo realizar la operación")
        
        return render_template("resultado.html", num1=num1, num2=num2, operador=operador, resultado=resultado)
    else:
        return render_template("calculadora_post_wtf.html", form=form)




@app.route('/')
def inicio():
#   return render_template("inicio.html")
    lista=[]
    for file in listdir(app.root_path+"/static/img/"):
        lista.append(file)
    for item in lista:
        print(item)
    return render_template("inicio2.html", lista = lista)

@app.route('/upload', methods =['get', 'post'])
def upload():
    # carga request.from y request.file
    form = UploadForm() 
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path + "/static/img" + filename)
        return redirect(url_for('inicio'))
    return render_template('upload.html', form = form)

