from typing import Optional, Literal
from sqlmodel import SQLModel, Field
from datetime import date

TableName = Literal[
    "pais",
    "region",
    "responsable_plantacion",
    "plantacion",
    "tipo_grano",
    "grano_en_plantacion",
    "variedad",
    "variedad_especial",
    "oferta",
    "aditivo",
    "anyadir",
    "tienda",
    "cliente",
    "carrito",
    "contiene",
    "cafetera",
    "tiene_cafetera",
    "var_en_cafetera",
    "receta",
]

table_names: list[TableName] = [
    "pais",
    "region",
    "responsable_plantacion",
    "plantacion",
    "tipo_grano",
    "grano_en_plantacion",
    "variedad",
    "variedad_especial",
    "oferta",
    "aditivo",
    "anyadir",
    "tienda",
    "cliente",
    "carrito",
    "contiene",
    "cafetera",
    "tiene_cafetera",
    "var_en_cafetera",
    "receta",
]


class Pais(SQLModel, table=True):
    __tablename__ = "pais"
    id_pais: Optional[str] = Field(default=None, primary_key=True)
    nombre: str


class Region(SQLModel, table=True):
    __tablename__ = "region"
    id_pais: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="pais.id_pais"
    )
    id_region: Optional[str] = Field(default=None, primary_key=True)
    nombre: str


class ResponsablePlantacion(SQLModel, table=True):
    __tablename__ = "responsable_plantacion"
    dni_responsable: Optional[str] = Field(default=None, primary_key=True)
    nombre_responsable: Optional[str] = None


class Plantacion(SQLModel, table=True):
    __tablename__ = "plantacion"
    id_pais: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="pais.id_pais"
    )
    id_region: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="region.id_region"
    )
    id_plantacion: Optional[str] = Field(default=None, primary_key=True)
    direccion: str
    dni_responsable: Optional[str] = Field(
        default=None, foreign_key="responsable_plantacion.dni_responsable"
    )


class TipoGrano(SQLModel, table=True):
    __tablename__ = "tipo_grano"
    id_tipo_grano: Optional[str] = Field(default=None, primary_key=True)
    descripcion: Optional[str] = None


class GranoEnPlantacion(SQLModel, table=True):
    __tablename__ = "grano_en_plantacion"
    id_pais: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="pais.id_pais"
    )
    id_region: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="region.id_region"
    )
    id_plantacion: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="plantacion.id_plantacion"
    )
    id_tipo_grano: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="tipo_grano.id_tipo_grano"
    )


class Variedad(SQLModel, table=True):
    __tablename__ = "variedad"
    id_variedad: Optional[str] = Field(default=None, primary_key=True)
    denominacion: str
    pvp10: float
    intensidad: int
    nivel_cafeina: Optional[str] = None


class VariedadEspecial(SQLModel, table=True):
    __tablename__ = "variedad_especial"
    id_variedad: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="variedad.id_variedad"
    )
    descripcion_envase: str
    fecha_inicio_disponibilidad: date
    fecha_fin_disponibilidad: date


class Oferta(SQLModel, table=True):
    __tablename__ = "oferta"
    id_variedad: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="variedad.id_variedad"
    )
    fecha_inicio: Optional[date] = None
    fecha_fin: date
    descuento: float
    fidelidad: Optional[str] = None


class Aditivo(SQLModel, table=True):
    __tablename__ = "aditivo"
    id_aditivo: Optional[str] = Field(default=None, primary_key=True)
    descripcion: Optional[str] = None


class Anyadir(SQLModel, table=True):
    __tablename__ = "anyadir"
    id_aditivo: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="aditivo.id_aditivo"
    )
    id_variedad: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="variedad.id_variedad"
    )
    cantidad: float


class Tienda(SQLModel, table=True):
    __tablename__ = "tienda"
    id_tienda: Optional[str] = Field(default=None, primary_key=True)
    direccion: str


class Cliente(SQLModel, table=True):
    __tablename__ = "cliente"
    dni: Optional[str] = Field(default=None, primary_key=True)
    nombre: str
    telefono: Optional[str] = None
    email: str
    fecha: date


class Carrito(SQLModel, table=True):
    __tablename__ = "carrito"
    id_tienda: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="tienda.id_tienda"
    )
    id_carrito: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    fecha: str
    dni_cliente: str = Field(foreign_key="cliente.dni")


class Contiene(SQLModel, table=True):
    __tablename__ = "contiene"
    id_tienda: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="tienda.id_tienda"
    )
    id_carrito: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="carrito.id_carrito"
    )
    id_variedad: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="variedad.id_variedad"
    )
    cantidad: Optional[int] = None


class Cafetera(SQLModel, table=True):
    __tablename__ = "cafetera"
    fabricante: Optional[str] = Field(default=None, primary_key=True)
    modelo: Optional[str] = Field(default=None, primary_key=True)
    presion: float


class TieneCafetera(SQLModel, table=True):
    __tablename__ = "tiene_cafetera"
    fabricante_caf: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="cafetera.fabricante"
    )
    modelo_caf: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="cafetera.modelo"
    )
    dni_cliente: Optional[str] = Field(default=None, foreign_key="cliente.dni")


class VarEnCafetera(SQLModel, table=True):
    __tablename__ = "var_en_cafetera"
    fabricante_caf: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="cafetera.fabricante"
    )
    modelo_caf: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="cafetera.modelo"
    )
    id_variedad: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="variedad.id_variedad"
    )


class Receta(SQLModel, table=True):
    __tablename__ = "receta"
    id_tipo_grano: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="tipo_grano.id_tipo_grano"
    )
    id_variedad: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="variedad.id_variedad"
    )
    cantidad: float
    nivel_molido: int
