from flask import Flask, render_template, redirect, url_for, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

userDB = "postgres"
passDB = "admin"
urlDB = "localhost"
nameDB = "sap_flash_db"

fullUrl = f"postgresql://{userDB}:{passDB}@{urlDB}/{nameDB}"

app.config['SQLALCHEMY_DATABASE_URI']=fullUrl
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

class Persona(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))
    
    def __str__(self):
        return (f"id: {self.id}"
                f"nombre: {self.nombre}"
                f"apellido: {self.apellido}"
                f"email: {self.email}")

migrate = Migrate()
migrate.init_app(app,db)


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    personas = Persona.query.all()
    totalPersonas = Persona.query.count()
    app.logger.debug(f'listados Persona: {personas}')
    app.logger.debug(f'Total Personas: {totalPersonas}')
    return render_template('index.html', personas=personas, totalPersonas=totalPersonas)


nombre = "escarcha"
edad = 25

@app.route('/saludar')
def salidar():
    return  f"hola {nombre} su edad es: {edad}"

@app.route('/mostrar/<nombre>', methods=['GET', 'POST'])
def mostrarNombre(nombre):
    return render_template('mostrar.html',myvariable=nombre)

@app.route('/redireccionar')
def redireccion():
    return redirect(url_for('inicio'))

@app.route('/salir')
def salir():
    return abort(404)

@app.errorhandler(404)
def paginaNoEncontrada(error):
    return render_template('error404.html',llaveError=error), 404

@app.route('/signup',methods=['GET','POST'])
def showSignupForm():
    if request.method == 'POST':
        name = request.form['name']
        first_name = request.form.get("name")
        email = request.form['email']
        password = request.form['password']
        next = request.args.get('next', None)
        if next:
            return redirect(next), {first_name}, name
        return redirect(url_for('respuestaForm'))
    return render_template("signupForm.html")

@app.route('/respuestaForm')
def respuestaForm():
    app.logger.info(f"entramos en el path {request.path}")
    return "datos ingresados"

@app.route('/form', methods=['GET','POST'])
def gfg():
    if request.method == 'POST':
        first_name = request.form.get("fname")
        last_name = request.form.get('lname')
        return f"Your name is {first_name} {last_name}"
    return render_template("form.html")