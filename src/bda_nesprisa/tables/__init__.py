from datetime import date
from typing import Callable
from faker import Faker
from bda_nesprisa.tables.types import (
    TableName,
    Pais,
    Region,
    ResponsablePlantacion,
    Plantacion,
    TipoGrano,
    GranoEnPlantacion,
    Variedad,
    VariedadEspecial,
    Oferta,
    Aditivo,
    Anyadir,
    Tienda,
    Cliente,
    Carrito,
    Contiene,
    Cafetera,
    TieneCafetera,
    VarEnCafetera,
    Receta,
)
from random import choice, randint, random
from bda_nesprisa.tables.helpers import create_dni, uuid, choose
from dateutil.relativedelta import relativedelta

fake = Faker("es_ES")


def create_pais(**_):
    return Pais(id_pais=uuid(), nombre=fake.country())


def create_region(pais_list: list[Pais], **_):
    return Region(
        id_pais=choice(pais_list).id_pais, id_region=uuid(), nombre=fake.region()
    )


def create_responsable_plantacion(**_):
    return ResponsablePlantacion(
        dni_responsable=create_dni(),
        nombre_responsable=fake.name(),
    )


def create_plantacion(
    region_list: list[Region],
    responsable_plantacion_list: list[ResponsablePlantacion],
    **_,
):
    region = choose(region_list)
    responsable = choose(responsable_plantacion_list)
    return Plantacion(
        id_pais=region.id_pais,
        id_region=region.id_region,
        id_plantacion=uuid(),
        direccion=fake.address(),
        dni_responsable=responsable.dni_responsable,
    )


def create_tipo_grano(**_):
    return TipoGrano(id_tipo_grano=uuid(), descripcion=fake.text()[:100])


def create_grano_en_plantacion(
    plantacion_list: list[Plantacion], tipo_grano_list: list[TipoGrano], **_
):
    plantacion = choose(plantacion_list)
    tipo_grano = choose(tipo_grano_list)
    return GranoEnPlantacion(
        id_pais=plantacion.id_pais,
        id_region=plantacion.id_region,
        id_plantacion=plantacion.id_plantacion,
        id_tipo_grano=tipo_grano.id_tipo_grano,
    )


def create_variedad(**_):
    return Variedad(
        id_variedad=uuid(),
        denominacion=fake.unique.word(),
        pvp10=random() * 100,
        intensidad=randint(0, 10),
        nivel_cafeina=choice([None, "bajo", "medio", "alto"]),
    )


def create_variedad_especial(variedad_list: list[Variedad], **_):
    variedad = choose(variedad_list)
    fecha_inicio_disponibilidad = date.fromisoformat(fake.date())
    fecha_fin_disponibilidad = fecha_inicio_disponibilidad + relativedelta(
        weeks=+randint(1, 8)
    )
    return VariedadEspecial(
        id_variedad=variedad.id_variedad,
        descripcion_envase=fake.text()[:100],
        fecha_inicio_disponibilidad=fecha_inicio_disponibilidad,
        fecha_fin_disponibilidad=fecha_fin_disponibilidad,
    )


def create_oferta(variedad_list: list[Variedad], **_):
    variedad = choose(variedad_list)
    fecha_inicio = date.fromisoformat(fake.date())
    fecha_fin = fecha_inicio + relativedelta(weeks=+randint(1, 8))
    return Oferta(
        id_variedad=variedad.id_variedad,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        descuento=random(),
        fidelidad=choice([None, "I", "II", "III"]),
    )


def create_aditivo(**_):
    return Aditivo(id_aditivo=uuid(), descripcion=fake.text()[:100])


def create_anyadir(aditivo_list: list[Aditivo], variedad_list: list[Variedad], **_):
    aditivo = choose(aditivo_list)
    variedad = choose(variedad_list)
    return Anyadir(
        id_aditivo=aditivo.id_aditivo,
        id_variedad=variedad.id_variedad,
        cantidad=random() * choose([1, 10, 100]),
    )


def create_tienda(**_):
    return Tienda(id_tienda=uuid(), direccion=fake.address()[:30])


def create_cliente(**_):
    return Cliente(
        dni=create_dni(),
        nombre=fake.name(),
        telefono=fake.phone_number().replace("+34", "").replace(" ", ""),
        email=fake.email(),
        fecha=date.fromisoformat(fake.date()),
    )


def create_carrito(tienda_list: list[Tienda], cliente_list: list[Cliente], **_):
    tienda = choose(tienda_list)
    cliente = choose(cliente_list)
    return Carrito(
        id_tienda=tienda.id_tienda,
        fecha=date.fromisoformat(fake.date()),
        dni_cliente=cliente.dni,
    )


def create_contiene(carrito_list: list[Carrito], variedad_list: list[Variedad], **_):
    carrito = choose(carrito_list)
    variedad = choose(variedad_list)
    return Contiene(
        id_tienda=carrito.id_tienda,
        id_carrito=carrito.id_carrito,
        id_variedad=variedad.id_variedad,
        cantidad=randint(0, 100),
    )


def create_cafetera(**_):
    return Cafetera(
        fabricante=fake.company(),
        modelo=fake.word(),
        presion=random() * 10,
    )


def create_tiene_cafetera(
    cafetera_list: list[Cafetera], cliente_list: list[Cliente], **_
):
    cafetera = choose(cafetera_list)
    cliente = choose(cliente_list)
    return TieneCafetera(
        fabricante_caf=cafetera.fabricante,
        modelo_caf=cafetera.modelo,
        dni_cliente=cliente.dni,
    )


def create_var_en_cafetera(
    cafetera_list: list[Cafetera], variedad_list: list[Variedad], **_
):
    cafatera = choose(cafetera_list)
    variedad = choose(variedad_list)
    return VarEnCafetera(
        fabricante_caf=cafatera.fabricante,
        modelo_caf=cafatera.modelo,
        id_variedad=variedad.id_variedad,
    )


def create_receta(tipo_grano_list: list[TipoGrano], variedad_list: list[Variedad], **_):
    tipo_grano = choose(tipo_grano_list)
    variedad = choose(variedad_list)
    return Receta(
        id_tipo_grano=tipo_grano.id_tipo_grano,
        id_variedad=variedad.id_variedad,
        cantidad=random() * 10,
        nivel_molido=randint(0, 5),
    )


create_table: dict[TableName, Callable] = {
    "pais": create_pais,
    "region": create_region,
    "responsable_plantacion": create_responsable_plantacion,
    "plantacion": create_plantacion,
    "tipo_grano": create_tipo_grano,
    "grano_en_plantacion": create_grano_en_plantacion,
    "variedad": create_variedad,
    "variedad_especial": create_variedad_especial,
    "oferta": create_oferta,
    "aditivo": create_aditivo,
    "anyadir": create_anyadir,
    "tienda": create_tienda,
    "cliente": create_cliente,
    "carrito": create_carrito,
    "contiene": create_contiene,
    "cafetera": create_cafetera,
    "tiene_cafetera": create_tiene_cafetera,
    "var_en_cafetera": create_var_en_cafetera,
    "receta": create_receta,
}


__all__ = ["create_table"]
