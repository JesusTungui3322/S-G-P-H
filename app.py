from flask import Flask, request, jsonify
from models import db, Paciente, Medico, Cita, HistorialMedico, Especialidad


app = Flask(__name__)


# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SECRET_KEY'] = 'JesusDiaz2323214234234234fdrefs'
db.init_app(app)


# CRUD para Paciente
@app.route('/pacientes', methods=['POST'])
def crear_paciente():
    data = request.get_json()
    cedula = Paciente.query.filter_by(cedula=data.get('cedula')).first()
    if cedula:
        return jsonify({'mensaje': 'cedula ya registrada'}), 401
    for parametro in data:
        if parametro not in ['nombre', 'apellido', 'cedula', 'historial_medico_detalles']:
            return jsonify({'mensaje': parametro + 'no es un parametro valido'}), 401
    historial_medico = data.get('historial_medico_detalles')
    historial_medico = HistorialMedico(detalles=historial_medico)
    db.session.add(historial_medico)
    db.session.commit()
    paciente = Paciente(historial_medico_id=historial_medico.id, nombre=data.get('nombre'), apellido=data.get('apellido'), cedula=data.get('cedula'))
    db.session.add(paciente)
    db.session.commit()
    return jsonify({'id': paciente.id}), 201


@app.route('/pacientes/<int:id>', methods=['GET'])
def obtener_paciente(id):
    paciente = Paciente.query.get(id)
    detalles_p =[]
    if not paciente:
        return jsonify({'id': 'id no registrado'}), 404
    historial = HistorialMedico.query.get(paciente.historial_medico_id)
    result = {'id': paciente.id, 'nombre': paciente.nombre, 'apellido': paciente.apellido, 'cedula': paciente.cedula, 'historial_medico': {'id': historial.id, 'detalles': historial.detalles}}
    detalles_p.append(result)
    return jsonify(detalles_p), 200


@app.route('/pacientes/<int:id>', methods=['PUT'])
def actualizar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({'mensaje': 'id no registrado'}), 404
    data = request.get_json()
    for parametro in data:
        if parametro not in ['nombre', 'apellido', 'cedula', 'historial_medico_detalles']:
            return jsonify({'mensaje': parametro + 'no es un parametro valido'}), 401
    historial = HistorialMedico.query.get(paciente.historial_medico_id)
    paciente.nombre = data.get('nombre', paciente.nombre)
    paciente.apellido = data.get('apellido', paciente.apellido)
    paciente.cedula = data.get('cedula', paciente.cedula)
    historial.detalles = data.get('historial_medico_detalles', historial.detalles)
    db.session.commit()
    return jsonify({'mensaje': 'paciente actualizado'}), 200


@app.route('/pacientes/<int:id>', methods=['DELETE'])
def eliminar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({'message': 'Paciente no registrado'}), 404
    db.session.delete(paciente)
    db.session.commit()
    return jsonify({'message': 'Paciente eliminado'}), 200


# CRUD para Médico
@app.route('/medicos', methods=['POST'])
def crear_medico():
    data = request.get_json()
    cedula = Medico.query.filter_by(cedula=data.get('cedula')).first()
    if cedula:
        return jsonify({'mensaje': 'cedula ya registrada'}), 401
    for parametro in data:
        if parametro not in ['nombre', 'apellido', 'cedula', 'especialidad_nombre', 'especialidad_descripcion']:
            return jsonify({'mensaje': parametro + ' no es un parametro valido'}), 401
    especialidad_n = data.get('especialidad_nombre')
    especialidad_d = data.get('especialidad_descripcion')
    especialidad = Especialidad(nombre=especialidad_n, descripcion=especialidad_d)
    db.session.add(especialidad)
    db.session.commit()
    medico = Medico(especialidad_id=especialidad.id, nombre=data.get('nombre'), apellido=data.get('apellido'), cedula=data.get('cedula'))
    db.session.add(medico)
    db.session.commit()
    return jsonify({'id': medico.id, 'mensaje': 'exitoso'}), 201


@app.route('/medicos/<int:id>', methods=['GET'])
def obtener_medico(id):
    medico = Medico.query.get(id)
    detalles_m =[]
    if not medico:
        return jsonify({'mensaje': 'id no registrado'}), 404
    especialidad = Especialidad.query.get(medico.especialidad_id)
    result = {'id': medico.id, 'nombre': medico.nombre, 'apellido': medico.apellido, 'cedula': medico.cedula, 'especialidad': {'id': especialidad.id, 'nombre': especialidad.nombre, 'descripcion': especialidad.descripcion}}
    detalles_m.append(result)
    return jsonify(detalles_m), 200


@app.route('/medicos/<int:id>', methods=['PUT'])
def actualizar_medico(id):
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({'mensaje': 'id no registrado'}), 404
    data = request.get_json()
    for parametro in data:
        if parametro not in ['nombre', 'apellido', 'cedula', 'especialidad_nombre', 'especialidad_descripcion']:
            return jsonify({'mensaje': parametro + ' no es un parametro valido'}), 401
    especialidad = Especialidad.query.get(medico.especialidad_id)
    medico.nombre = data.get('nombre', medico.nombre)
    medico.apellido = data.get('apellido', medico.apellido)
    medico.cedula = data.get('cedula', medico.cedula)
    especialidad.nombre = data.get('epecialidad_nombre', especialidad.nombre)
    especialidad.descripcion = data.get('especialidad_descripcion', especialidad.descripcion)
    db.session.commit()
    return jsonify({'mensaje': 'medico actualizado'}), 200


@app.route('/medicos/<int:id>', methods=['DELETE'])
def eliminar_medico(id):
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({'mensaje': 'id no encontrado'}), 404
    db.session.delete(medico)
    db.session.commit()
    return jsonify({'mensaje': 'medico eliminado'}), 200


# CRUD para Cita
@app.route('/citas', methods=['POST'])
def crear_cita():
    data = request.get_json()
    for parametro in data:
        if parametro not in ['paciente_id', 'medico_id']:
            return jsonify({'mensaje': parametro + ' no es un parametro valido'}), 401
    paciente = Paciente.query.get(data.get('paciente_id'))
    medico = Medico.query.get(data.get('medico_id'))
    if not paciente or not medico:
        return jsonify({'mensaje': 'paciente o medico no registrado'}), 404
    cita = Cita(paciente_id=paciente.id, medico_id=medico.id)
    db.session.add(cita)
    db.session.commit()
    return jsonify({'id': cita.id}), 201


@app.route('/citas/<int:id>', methods=['GET'])
def obtener_cita(id):
    cita = Cita.query.get(id)
    detalles_c = []
    if not cita:
        return jsonify({'mensaje': 'id no registrado'})
    paciente = Paciente.query.get(cita.paciente_id)
    historial = HistorialMedico.query.get(paciente.historial_medico_id)
    medico = Medico.query.get(cita.medico_id)
    especialidad = Especialidad.query.get(medico.especialidad_id)
    result = {'id': cita.id, 'fecha': cita.fecha, 'paciente': {'id': paciente.id, 'nombre': paciente.nombre, 'apellido': paciente.apellido, 'cedula': paciente.cedula, 'historial_medico': {'id': historial.id, 'detalles': historial.detalles}}, 'medico': {'id': medico.id, 'nombre': medico.nombre, 'apellido': medico.apellido, 'cedula': medico.cedula, 'especialidad': {'id': especialidad.id, 'nombre': especialidad.nombre, 'descripcion': especialidad.descripcion}}}
    detalles_c.append(result)
    return jsonify(detalles_c), 200


@app.route('/citas/<int:id>', methods=['DELETE'])
def eliminar_cita(id):
    cita = Cita.query.get(id)
    if not cita:
        return jsonify({'message': 'Cita no registrado'}), 404
    db.session.delete(cita)
    db.session.commit()
    return jsonify({'message': 'Cita eliminado'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')