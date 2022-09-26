from  flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request,flash,redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
#Add Database 
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root@127.0.0.1/examen"
app.config['SECRET_KEY']='My super secret that no one is supposed to know'
#Initialize the Database
db =SQLAlchemy(app)


class Estudiante(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    DNI=db.Column(db.Integer,unique=True)
    Apellidos = db.Column(db.String(64),nullable=False)
    Nombres= db.Column(db.String(128),nullable=False)
    FechaNacimento=db.Column(db.DateTime)
    Sexo=db.Column(db.String(10))
    escuela_est= db.relationship('Matricula', backref='estudiante', lazy=True)

#Create Model

class Curso(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Codigo = db.Column(db.String(100),unique=True)
    Nombre= db.Column(db.String(200), nullable=False)
    Credito = db.Column(db.Integer, nullable=False)
    escuela_cur= db.relationship('Matricula', backref='curso', lazy=True)

class Escuela(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Codigo = db.Column(db.String(200), unique=True)
    Nombre= db.Column(db.String(200), nullable=False)
    Duracion = db.Column(db.Integer, nullable=False)
    escuela_est= db.relationship('Matricula', backref='escuela', lazy=True)

class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    escuela_id= db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
@app.route('/')
def index():
    return render_template('index.html')

#Create form class
class EstudianteForm(FlaskForm):
    DNI=StringField('DNI', validators=[DataRequired()])
    Apellidos=StringField('apellidos', validators=[DataRequired()])
    Nombres=StringField('nombres', validators=[DataRequired()])
    FechaNacimento=StringField('FechaNacimiento', validators=[DataRequired()])
    Sexo=StringField('sexo', validators=[DataRequired()])

class CursoForm(FlaskForm):
    Codigo=StringField('codigo', validators=[DataRequired()])
    Nombre=StringField('nombre', validators=[DataRequired()])
    Credito=StringField('Credito', validators=[DataRequired()])
    
class EscuelaForm(FlaskForm):
    Codigo=StringField('codigo', validators=[DataRequired()])
    Nombre=StringField('nombre', validators=[DataRequired()])
    Duracion=StringField('duracion', validators=[DataRequired()])


@app.route('/estudiante',methods=['GET','POST'])
def estudiante():
    form = EstudianteForm()
    if form.validate_on_submit():
        estudiante = Estudiante.query.filter_by(DNI=form.DNI.data).first()
        if estudiante is None:
            estudiante = Estudiante(DNI=form.DNI.data,Apellidos= form.Apellidos.data,Nombres= form.Nombres.data,
            FechaNacimiento=form.FechaNacimento.data,Sexo=form.Sexo.data)
            db.session.add(estudiante)
            db.session.commit()
        flash("Usuario añadido con exito")
        return redirect(url_for("index"))
    else:    return render_template('estudiante.html',form=form)

@app.route('/curso',methods=['GET','POST'])
def curso():
    form = CursoForm()
    if form.validate_on_submit():
        curso = Curso.query.filter_by(Codigo=form.Codigo.data).first()
        if curso is None:
            curso = Curso(Codigo=form.Codigo.data,Nombre=form.Nombre.data,Credito=form.Credito.data)
            db.session.add(curso)
            db.session.commit()
        flash("Usuario añadido con exito")
        return redirect(url_for("index"))
    else:    return render_template('curso.html',form=form)

@app.route('/escuela',methods=['GET','POST'])
def escuela():
    form = EscuelaForm()
    if form.validate_on_submit():
        escuela= Escuela.query.filter_by(Codigo= form.Codigo.data).first()
        if escuela is None:
            escuela = Escuela(Codigo=form.Codigo.data,Nombre= form.Nombre.data,Duracion=form.Duracion.data)
            db.session.add(escuela)
            db.session.commit()
        flash("Usuario añadido con exito")
        return redirect(url_for("index"))
    else:    return render_template('escuela.html',form=form)

def matricula():
    matriculaS=Matricula.query.order_by(Matricula.id)
    lista=[]
    for matricula in matriculaS:
        estudiante = Estudiante.query.filter_by(id=matricula.estudiante_id).first()
        escuela = Escuela.query.filter_by(id=matricula.escuela_id).first()
        curso = Curso.query.filter_by(id=matricula.curso_id).first()
        lista.append({
            "nombreEscuela":escuela.nombre,
            "nombreCurso":curso.nombre,
            "nombreEstudiante":estudiante.nombre})









