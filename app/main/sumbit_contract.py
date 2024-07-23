from flask import Blueprint, request, jsonify
from ..models.contract import Contract
from ..models.creations_record import CreationRecord
from ..models.content_contract import Contenido_Contrato
from .. import db

contract_blueprint = Blueprint('contract', __name__)

@contract_blueprint.route('/submit_contract', methods=['POST'])
def submit_contract():
    data = request.get_json()
    new_contract = Contract(
        fecha_inicio=data['fecha_inicio'],
        fecha_expiracion=data['fecha_expiracion'],
        comentario=data['comentario'],
        contrato=data['contrato']
    )
    db.session.add(new_contract)
    db.session.flush()  # Esto garantiza que se genera el id_contrato antes de usarlo

    # Crear y añadir contenido del contrato
    new_content = Contenido_Contrato(
        id_contrato=new_contract.id_contrato,
        nombres=data.get('nombres'),
        apellidos=data.get('apellidos'),
        direccion=data.get('direccion'),
        estado_civil=data.get('estado_civil'),
        fecha_nacimiento=data.get('fecha_nacimiento'),
        rut=data.get('rut'),
        mail=data.get('mail'),
        nacionalidad=data.get('nacionalidad'),
        sistema_salud=data.get('sistema_salud'),
        afp=data.get('afp'),
        nombre_empleador=data.get('nombre_empleador'),
        rut_empleador=data.get('rut_empleador'),
        cargo=data.get('cargo'),
        fecha_inicio=data.get('fecha_inicio'),
        fecha_final=data.get('fecha_final'),
        indefinido=data.get('indefinido'),
        sueldo_base=data.get('sueldo_base'),
        asignacio_colacion=data.get('asignacio_colacion'),
        bono_asistencia=data.get('bono_asistencia')
    )
    db.session.add(new_content)

    # Creación de registros de creación para cada usuario asignado
    for user_id in data['user_ids']:
        new_creation_record = CreationRecord(id_contrato=new_contract.id_contrato, id_usuario=user_id)
        db.session.add(new_creation_record)

    db.session.commit()
    return jsonify({
        "contract": new_contract.to_dict(),
        "content": new_content.to_dict()
    }), 201
