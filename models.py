from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


# Entidad Paciente
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(8), nullable=False, unique=True)
    historial_medico_id = db.Column(db.Integer, db.ForeignKey('historial_medico.id'), nullable=False)


# Entidad Médico
class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(100), nullable=False, unique=True)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidad.id'), nullable=False)


# Entidad Cita
class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=datetime.now)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)


# Entidad Historial Médico
class HistorialMedico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    detalles = db.Column(db.Text, nullable=False)


# Entidad Especialidad
class Especialidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)