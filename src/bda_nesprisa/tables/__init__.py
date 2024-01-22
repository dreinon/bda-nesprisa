from typing import Callable, NoReturn, TypedDict
from tqdm import tqdm
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


# FAKE DATA GENERATION

# 1. We use the Faker library with the Spanish locale to generate fake data
from faker import Faker

fake = Faker("es_ES")

# 2. We also defined helper functions to generate random DNI and UUID values
from bda_nesprisa.tables.helpers import create_dni, uuid

# 3. We use date to parse the dates from the fake data and relativedelta to generate dates that have to meet certain time constraints
from datetime import date
from dateutil.relativedelta import relativedelta

# 4. We use random to generate random values and choice to choose a random value from a list
from random import choice, randint, random


# DATA GENERATION FUNCTIONS

# We define a function for each table that returns a list of rows for that table

# Each function has dependency parameters defined as {table_name}_list which will be passed as kwargs
# and use **_ parameter to ignore any other parameters that we don't need

# We make sure no unique constrainsts are violated by checking the unique keys of the rows that have already been created
# We use the product function from itertools to generate all the possible combinations of the unique keys
from itertools import product


def create_pais(num_rows: int, pbar: tqdm, **_):
    rows: list[Pais] = []
    for _ in range(num_rows):
        rows.append(Pais(id_pais=uuid(), nombre=fake.country()))
        pbar.update()
    return rows


def create_region(pais_list: list[Pais], num_rows: int, pbar: tqdm, **_):
    rows: list[Region] = []
    for _ in range(num_rows):
        rows.append(
            Region(
                id_pais=choice([pais.id_pais for pais in pais_list]),
                id_region=uuid(),
                nombre=fake.region(),
            )
        )
        pbar.update()
    return rows


def create_responsable_plantacion(num_rows: int, pbar: tqdm, **_):
    rows: list[ResponsablePlantacion] = []
    for _ in range(num_rows):
        rows.append(
            ResponsablePlantacion(
                dni_responsable=create_dni(),
                nombre_responsable=fake.name(),
            )
        )
        pbar.update()
    return rows


def create_plantacion(
    region_list: list[Region],
    responsable_plantacion_list: list[ResponsablePlantacion],
    num_rows: int,
    pbar: tqdm,
    **_,
):
    rows: list[Plantacion] = []
    possible_uniques = list(
        product(
            [(region.id_pais, region.id_region) for region in region_list],
            [
                responsable.dni_responsable
                for responsable in responsable_plantacion_list
            ],
        )
    )
    for _ in range(num_rows):
        chosen_unique = choice(
            [
                chosen_unique
                for chosen_unique in possible_uniques
                if chosen_unique
                not in [
                    ((row.id_pais, row.id_region), row.dni_responsable) for row in rows
                ]
            ]
        )
        rows.append(
            Plantacion(
                id_pais=chosen_unique[0][0],
                id_region=chosen_unique[0][1],
                id_plantacion=uuid(),
                direccion=fake.address(),
                dni_responsable=chosen_unique[1],
            )
        )
        pbar.update()
    return rows


def create_tipo_grano(num_rows: int, pbar: tqdm, **_):
    rows: list[TipoGrano] = []
    for _ in range(num_rows):
        rows.append(TipoGrano(id_tipo_grano=uuid(), descripcion=fake.text()[:100]))
        pbar.update()
    return rows


def create_grano_en_plantacion(
    plantacion_list: list[Plantacion],
    tipo_grano_list: list[TipoGrano],
    num_rows: int,
    pbar: tqdm,
    **_,
):
    rows: list[GranoEnPlantacion] = []
    possible_uniques = list(
        product(
            [
                (plantacion.id_pais, plantacion.id_region, plantacion.id_plantacion)
                for plantacion in plantacion_list
            ],
            [tipo_grano.id_tipo_grano for tipo_grano in tipo_grano_list],
        )
    )
    for _ in range(num_rows):
        chosen_unique = choice(
            [
                chosen_unique
                for chosen_unique in possible_uniques
                if chosen_unique
                not in [
                    (
                        (row.id_pais, row.id_region, row.id_plantacion),
                        row.id_tipo_grano,
                    )
                    for row in rows
                ]
            ]
        )
        rows.append(
            GranoEnPlantacion(
                id_pais=chosen_unique[0][0],
                id_region=chosen_unique[0][1],
                id_plantacion=chosen_unique[0][2],
                id_tipo_grano=chosen_unique[1],
            )
        )
        pbar.update()
    return rows


def create_variedad(num_rows: int, pbar: tqdm, **_):
    rows: list[Variedad] = []
    for _ in range(num_rows):
        rows.append(
            Variedad(
                id_variedad=uuid(),
                denominacion=fake.unique.word(),
                pvp10=random() * 100,
                intensidad=randint(0, 10),
                nivel_cafeina=choice([None, "bajo", "medio", "alto"]),
            )
        )
        pbar.update()
    return rows


def create_variedad_especial(
    variedad_list: list[Variedad], num_rows: int, pbar: tqdm, **_
):
    rows: list[VariedadEspecial] = []
    possible_uniques = [variedad.id_variedad for variedad in variedad_list]

    for _ in range(num_rows):
        fecha_inicio_disponibilidad = date.fromisoformat(fake.date())
        fecha_fin_disponibilidad = fecha_inicio_disponibilidad + relativedelta(
            weeks=+randint(1, 8)
        )
        chosen_unique = choice(
            [
                chosen_unique
                for chosen_unique in possible_uniques
                if chosen_unique not in [row.id_variedad for row in rows]
            ]
        )

        rows.append(
            VariedadEspecial(
                id_variedad=chosen_unique,
                descripcion_envase=fake.text()[:100],
                fecha_inicio_disponibilidad=fecha_inicio_disponibilidad,
                fecha_fin_disponibilidad=fecha_fin_disponibilidad,
            )
        )
        pbar.update()
    return rows


def create_oferta(variedad_list: list[Variedad], num_rows: int, pbar: tqdm, **_):
    rows: list[Oferta] = []
    possible_uniques = [variedad.id_variedad for variedad in variedad_list]

    for _ in range(num_rows):
        fecha_inicio = date.fromisoformat(fake.date())
        fecha_fin = fecha_inicio + relativedelta(weeks=+randint(1, 8))
        chosen_unique = choice(
            [
                chosen_unique
                for chosen_unique in possible_uniques
                if (chosen_unique, fecha_inicio) not in [(row.id_variedad, row.fecha_inicio) for row in rows]
            ]
        )

        rows.append(
            Oferta(
                id_variedad=chosen_unique,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                descuento=random(),
                fidelidad=choice([None, "I", "II", "III"]),
            )
        )
        pbar.update()
    return rows


def create_aditivo(num_rows: int, pbar: tqdm, **_):
    rows: list[Aditivo] = []
    for _ in range(num_rows):
        rows.append(Aditivo(id_aditivo=uuid(), descripcion=fake.text()[:100]))
        pbar.update()
    return rows


def create_anyadir(
    aditivo_list: list[Aditivo],
    variedad_list: list[Variedad],
    num_rows: int,
    pbar: tqdm,
    **_,
):
    rows: list[Anyadir] = []
    possible_uniques = list(
        product(
            [aditivo.id_aditivo for aditivo in aditivo_list],
            [variedad.id_variedad for variedad in variedad_list],
        )
    )
    for _ in range(num_rows):
        chosen_unique = choice(
            [
                chosen_unique
                for chosen_unique in possible_uniques
                if chosen_unique
                not in [(row.id_aditivo, row.id_variedad) for row in rows]
            ]
        )
        rows.append(
            Anyadir(
                id_aditivo=chosen_unique[0],
                id_variedad=chosen_unique[1],
                cantidad=random() * choice([1, 10, 100]),
            )
        )
        pbar.update()
    return rows


def create_tienda(num_rows: int, pbar: tqdm, **_):
    rows: list[Tienda] = []
    for _ in range(num_rows):
        rows.append(Tienda(id_tienda=uuid(), direccion=fake.address()[:30]))
        pbar.update()
    return rows


def create_cliente(num_rows: int, pbar: tqdm, **_):
    rows: list[Cliente] = []
    for _ in range(num_rows):
        rows.append(
            Cliente(
                dni=create_dni(),
                nombre=fake.name(),
                telefono=fake.phone_number().replace("+34", "").replace(" ", ""),
                email=fake.email(),
                fecha=date.fromisoformat(fake.date()),
            )
        )
        pbar.update()
    return rows


def create_carrito(
    tienda_list: list[Tienda],
    cliente_list: list[Cliente],
    num_rows: int,
    pbar: tqdm,
    **_,
):
    rows: list[Carrito] = []
    for _ in range(num_rows):
        rows.append(
            Carrito(
                id_tienda=choice(tienda_list).id_tienda,
                dni_cliente=choice(cliente_list).dni,
                fecha=date.fromisoformat(fake.date()),
            )
        )
        pbar.update()
    return rows


def create_contiene(
    carrito_list: list[Carrito],
    variedad_list: list[Variedad],
    num_rows: int,
    pbar: tqdm,
    **_,
):
    rows: list[Contiene] = []
    possible_uniques = list(
        product(
            [(carrito.id_tienda, carrito.id_carrito) for carrito in carrito_list],
            [variedad.id_variedad for variedad in variedad_list],
        )
    )
    for _ in range(num_rows):
        chosen_unique = choice(
            [
                chosen_unique
                for chosen_unique in possible_uniques
                if chosen_unique
                not in [
                    ((row.id_tienda, row.id_carrito), row.id_variedad) for row in rows
                ]
            ]
        )
        rows.append(
            Contiene(
                id_tienda=chosen_unique[0][0],
                id_carrito=chosen_unique[0][1],
                id_variedad=chosen_unique[1],
                cantidad=randint(0, 100),
            )
        )
        pbar.update()
    return rows


def create_cafetera(num_rows: int, pbar: tqdm, **_):
    rows: list[Cafetera] = []
    for _ in range(num_rows):
        rows.append(
            Cafetera(
                fabricante=fake.company(),
                modelo=fake.word(),
                presion=random() * 10,
            )
        )
        pbar.update()
    return rows


def create_tiene_cafetera(
    cafetera_list: list[Cafetera],
    cliente_list: list[Cliente],
    num_rows: int,
    pbar: tqdm,
    **_,
):
    rows: list[TieneCafetera] = []
    possible_uniques = list(
        product(
            [(cafetera.fabricante, cafetera.modelo) for cafetera in cafetera_list],
            [cliente.dni for cliente in cliente_list],
        )
    )
    for _ in range(num_rows):
        chosen_unique = choice(
            [
                chosen_unique
                for chosen_unique in possible_uniques
                if chosen_unique
                not in [
                    ((row.fabricante_caf, row.modelo_caf), row.dni_cliente)
                    for row in rows
                ]
            ]
        )
        rows.append(
            TieneCafetera(
                fabricante_caf=chosen_unique[0][0],
                modelo_caf=chosen_unique[0][1],
                dni_cliente=chosen_unique[1],
            )
        )
        pbar.update()
    return rows


def create_var_en_cafetera(
    cafetera_list: list[Cafetera],
    variedad_list: list[Variedad],
    num_rows: int,
    pbar: tqdm,
    **_,
):
    rows: list[VarEnCafetera] = []
    possible_uniques = list(
        product(
            [(cafetera.fabricante, cafetera.modelo) for cafetera in cafetera_list],
            [variedad.id_variedad for variedad in variedad_list],
        )
    )
    for _ in range(num_rows):
        chosen_unique = choice(
            [
                chosen_unique
                for chosen_unique in possible_uniques
                if chosen_unique
                not in [
                    ((row.fabricante_caf, row.modelo_caf), row.id_variedad)
                    for row in rows
                ]
            ]
        )
        rows.append(
            VarEnCafetera(
                fabricante_caf=chosen_unique[0][0],
                modelo_caf=chosen_unique[0][1],
                id_variedad=chosen_unique[1],
            )
        )
        pbar.update()
    return rows


def create_receta(
    tipo_grano_list: list[TipoGrano],
    variedad_list: list[Variedad],
    num_rows: int,
    pbar: tqdm,
    **_,
):
    rows: list[Receta] = []
    possible_uniques = list(
        product(
            [tipo_grano.id_tipo_grano for tipo_grano in tipo_grano_list],
            [variedad.id_variedad for variedad in variedad_list],
        )
    )
    for _ in range(num_rows):
        chosen_unique = choice(
            [
                chosen_unique
                for chosen_unique in possible_uniques
                if chosen_unique
                not in [(row.id_tipo_grano, row.id_variedad) for row in rows]
            ]
        )
        rows.append(
            Receta(
                id_tipo_grano=chosen_unique[0],
                id_variedad=chosen_unique[1],
                cantidad=random() * 10,
                nivel_molido=randint(0, 5),
            )
        )
        pbar.update()
    return rows


# We define a dict that for each table contains the function to create the rows
# and the number of rows to create in order to be able to iterate over it in the main function
# NOTE: the values of the number of rows to create for each table have been fine-tuned for
#       the example so the script does not take so long and applying common-sense to the meaning of each table
CreateRowsDictValue = TypedDict(
    "CreateRowsDictValue", {"fn": Callable, "num_rows": int}
)
create_rows: dict[TableName, CreateRowsDictValue] = {
    "pais": {
        "fn": create_pais,
        "num_rows": 100,
    },
    "region": {
        "fn": create_region,
        "num_rows": 200,
    },
    "responsable_plantacion": {
        "fn": create_responsable_plantacion,
        "num_rows": 100,
    },
    "plantacion": {
        "fn": create_plantacion,
        "num_rows": 10,
    },
    "tipo_grano": {
        "fn": create_tipo_grano,
        "num_rows": 10,
    },
    "grano_en_plantacion": {
        "fn": create_grano_en_plantacion,
        "num_rows": 50,
    },
    "variedad": {
        "fn": create_variedad,
        "num_rows": 20,
    },
    "variedad_especial": {
        "fn": create_variedad_especial,
        "num_rows": 5,
    },
    "oferta": {
        "fn": create_oferta,
        "num_rows": 50,
    },
    "aditivo": {
        "fn": create_aditivo,
        "num_rows": 3,
    },
    "anyadir": {
        "fn": create_anyadir,
        "num_rows": 10,
    },
    "tienda": {
        "fn": create_tienda,
        "num_rows": 50,
    },
    "cliente": {
        "fn": create_cliente,
        "num_rows": 50,
    },
    "carrito": {
        "fn": create_carrito,
        "num_rows": 50,
    },
    "contiene": {
        "fn": create_contiene,
        "num_rows": 200,
    },
    "cafetera": {
        "fn": create_cafetera,
        "num_rows": 30,
    },
    "tiene_cafetera": {
        "fn": create_tiene_cafetera,
        "num_rows": 200,
    },
    "var_en_cafetera": {
        "fn": create_var_en_cafetera,
        "num_rows": 200,
    },
    "receta": {
        "fn": create_receta,
        "num_rows": 100,
    },
}

# We only export the create_rows dict since we don't want to expose the create_rows functions outside
__all__ = ["create_rows"]
