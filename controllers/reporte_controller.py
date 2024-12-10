from flask import Blueprint, render_template
from models.asistencia_model import Asistencia
from models.estudiante_model import Estudiante
from sqlalchemy import case, func
from database import db

# Crear el Blueprint
reporte_bp = Blueprint('reportes', __name__)

# Ruta para ver el reporte general de asistencias
@reporte_bp.route('/')
def reporte_general():
    # Obtener datos de asistencia agrupados por estudiante
    resultados = (
        db.session.query(
            Estudiante.id,
            Estudiante.nombre,
            Estudiante.apellido,
            func.count(Asistencia.id).label('total_asistencias'),
            func.sum(
                case(
                    (Asistencia.estado == 'Presente', 1),  # Cambio: se pasa como argumento posicional
                    else_=0  # else sigue siendo válido
                )
            ).label('total_presentes'),
        )
        .join(Asistencia, Estudiante.id == Asistencia.estudiante_id, isouter=True)
        .group_by(Estudiante.id)
        .all()
    )

    # Calcular porcentaje de asistencia
    reporte = []
    for r in resultados:
        porcentaje = (r.total_presentes / r.total_asistencias) * 100 if r.total_asistencias > 0 else 0
        reporte.append({
            'id': r.id,
            'nombre': r.nombre,
            'apellido': r.apellido,
            'total_asistencias': r.total_asistencias,
            'total_presentes': r.total_presentes,
            'porcentaje_asistencia': round(porcentaje, 2),
        })

    return render_template('reporte/general.html', reporte=reporte)
