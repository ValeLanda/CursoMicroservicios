from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Date,
    null,
)
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.expression import false
from model.domain.base_model import BaseModel
from model.domain.cat_estatus_sol_model import CatEstatusSolicitudModel
from model.domain.celular_prospecto_model import CelularProspectoModel
from model.domain.cliente_model import ClienteModel
from model.domain.direccion_cliente_model import DireccionClienteModel
from model.domain.direccion_prospecto_model import DireccionProspectoModel
from model.domain.email_model import EmailModel
from model.domain.login_model import LoginModel
from model.domain.prospecto_model import ProspectoModel

metadata = MetaData()
################################################################################
### Se debe de realizar el mapeo entre clases de negocio y la base de datos
### el mapeo se hace del modo "tradicional" de SQLAlquemy
################################################################################
tabla_ejemplo = Table(
    "tbc_hawk_alert",
    metadata,
    Column("idHawkAlert", Integer, primary_key=True, autoincrement=True),
    Column("C_FechaReporte", Date, nullable=True),
    Column("C_CodigoClave", Integer, nullable=True),
    Column("C_TipoInstitucion", String(45), nullable=True),
    Column("C_Mensaje", String(60), nullable=True),
    Column("BD_CodigoClave", Integer, nullable=True),
    Column("BD_TipoInstitucion", String(45), nullable=True),
    Column("BD_Mensaje", String(60), nullable=True),
    Column("fbid", String(20), nullable=False),
    Column("idRespuesta", Integer, nullable=True),
)

tbl_email = Table(
    "tbl_email",
    metadata,
    Column("id_email", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("email", String(50), nullable=False, unique=True)
)

tbl_cat_estatus_sol = Table(
    "cat_estatus_sol",
    metadata,
    Column("id_estatus", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("estatus", String(50), nullable=False, unique=True)
)

tbl_login = Table(
    "tbl_login",
    metadata,
    Column("id_login", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("estatus", String(50), nullable=False, unique=True)
)

tbl_prospecto = Table(
    "tbl_prospecto",
    metadata,
    Column("id_prospecto", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("id_email", Integer, nullable=False),
    Column("id_estatus_sol", Integer, default=null),
    Column("primer_nombre", String(30), nullable=False),
    Column("segundo_nombre", String(30), default=null),
    Column("ap_paterno", String(50), nullable=False),
    Column("ap_materno", String(50)),
    Column("CURP", String(20), nullable=False),
    Column("fecha_nac", Date, default=null),
    Column("RFC", String(20), nullable=False)
)

tbl_direccion_sol = Table(
    "tbl_direccion_sol",
    metadata,
    Column("id_direccion", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("id_sol", Integer, nullable=False),
    Column("calle", String(50), nullable=False, unique=True)
)

tbl_celular = Table(
    "tbl_celular",
    metadata,
    Column("id_tel", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("tel", String(5), nullable=False, unique=True),
    Column("id_sol", Integer, nullable=False)
)

tbl_cliente = Table(
    "tbl_cliente",
    metadata,
    Column("id_cliente", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("num_cte", String(30), nullable=False),
    Column("email", String(50), nullable=False),
    Column("primer_nombre", String(30), nullable=False),
    Column("segundo_nombre", String(30)),
    Column("ap_paterno", String(50), nullable=False),
    Column("ap_materno", String(50)),
    Column("CURP", String(20), nullable=False),
    Column("fecha_nac", Date, default=null),
    Column("celular", String(20), nullable=False),
    Column("RFC", String(20), nullable=False)
)

tbl_direccion_cte = Table(
    "tbl_direccion_cte",
    metadata,
    Column("id_direccion", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("id_cliente", Integer),
    Column("calle", String(50), nullable=False, unique=True)
)

################################################################################
### Este método se llama al inicio del programa, no se debe de cambiar el
### nombre de la función y debe de contener todos los mapeos
################################################################################
def start_mappers():
    mapper(BaseModel, tabla_ejemplo, properties={
        'Id': tabla_ejemplo.c.idHawkAlert,
        'FechaReporte': tabla_ejemplo.c.C_FechaReporte,
        'CodigoClave': tabla_ejemplo.c.C_CodigoClave,
        'TipoInstitucion': tabla_ejemplo.c.C_TipoInstitucion,
        'Mensaje': tabla_ejemplo.c.C_Mensaje,
        'FacebookId': tabla_ejemplo.c.fbid,
        'Respuesta': tabla_ejemplo.c.idRespuesta,
    })

    mapper(EmailModel, tbl_email, properties={
        'IdEmail': tbl_email.c.id_email,
        'Email': tbl_email.c.email
    })

    mapper(CatEstatusSolicitudModel, tbl_cat_estatus_sol, properties={
        'IdEstatus': tbl_cat_estatus_sol.c.id_estatus,
        'Estatus': tbl_cat_estatus_sol.c.estatus
    })

    mapper(LoginModel, tbl_login, properties={
        'IdLogin': tbl_login.c.id_login,
        'Estatus': tbl_login.c.estatus
    })

    mapper(ProspectoModel, tbl_prospecto, properties={
        'IdProspecto': tbl_prospecto.c.id_prospecto,
        'IdEmail': tbl_prospecto.c.id_email,
        'IdEstatusSolicitud': tbl_prospecto.c.id_estatus_sol,
        'PrimerNombre': tbl_prospecto.c.primer_nombre,
        'SegundoNombre': tbl_prospecto.c.segundo_nombre,
        'ApellidoPaterno': tbl_prospecto.c.ap_paterno,
        'ApellidoMaterno': tbl_prospecto.c.ap_materno,
        'CURP': tbl_prospecto.c.CURP,
        'FechaNacimiento': tbl_prospecto.c.fecha_nac,
        'RFC': tbl_prospecto.c.RFC,
    })

    mapper(DireccionProspectoModel, tbl_direccion_sol, properties={
        'IdDireccion': tbl_direccion_sol.c.id_direccion,
        'IdSolicitud': tbl_direccion_sol.c.id_sol,
        'Calle': tbl_direccion_sol.c.calle
    })

    mapper(CelularProspectoModel, tbl_celular, properties={
        'IdTelefono': tbl_celular.c.id_tel,
        'Telefono': tbl_celular.c.tel,
        'IdSolicitud': tbl_celular.c.id_sol
    })

    mapper(ClienteModel, tbl_cliente, properties={
        'IdCliente': tbl_cliente.c.id_cliente,
        'NumeroCliente': tbl_cliente.c.num_cte,
        'Email': tbl_cliente.c.email,
        'PrimerNombre': tbl_cliente.c.primer_nombre,
        'SegundoNombre': tbl_cliente.c.segundo_nombre,
        'ApellidoPaterno': tbl_cliente.c.ap_paterno,
        'ApellidoMaterno': tbl_cliente.c.ap_materno,
        'CURP': tbl_cliente.c.CURP,
        'FechaNacimiento': tbl_cliente.c.fecha_nac,
        'Celular': tbl_cliente.c.celular,
        'RFC': tbl_cliente.c.RFC,
    })

    mapper(DireccionClienteModel, tbl_direccion_cte, properties={
        'IdDireccion': tbl_direccion_cte.c.id_direccion,
        'IdCliente': tbl_direccion_cte.c.id_cliente,
        'Calle': tbl_direccion_cte.c.calle
    })