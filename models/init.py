from .expediente_model import ExpedienteModel
from .propietario_model import PropietarioModel
from .expediente_propietario_model import Expediente_PropietarioModel
from .tipoObra_model import TipoObraModel
from .expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
from .estadoInspeccion_model import EstadoInspeccionModel
from .estadoExpediente_model  import EstadoExpedienteModel
from .inspector_model import InspectorModel
from .profesional_model import ProfesionalModel
from .tipoExpediente_model import TipoExpedienteModel
from .tipoProfesion_model import TipoProfesionModel


__all__ = [
    "ExpedienteModel",
    "PropietarioModel",
    "ProfesionalModel",
    "Expediente_PropietarioModel",
    "TipoObraModel",
    "Expediente_EstadoExpedienteModel",
    "EstadoInspeccionModel",
    "EstadoExpedienteModel",
    "InspectorModel",
    "TipoExpedienteModel",
    "TipoProfesionModel",
]