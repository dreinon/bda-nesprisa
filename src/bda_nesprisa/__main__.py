from copy import deepcopy
from bda_nesprisa.tables.types import TableName, table_names
from bda_nesprisa.tables import create_table
from sqlmodel import Session, create_engine

ENGINE_STRING = "oracle+oracledb://CDA14:BDA@oralabos.dsic.upv.es:1521/labora"

rows: dict[TableName, list] = {table: [] for table in table_names}


def main(engine=create_engine(ENGINE_STRING)):
    with Session(engine, expire_on_commit=False) as session:
        for table in table_names:
            rows_list = {f"{k}_list": v for k, v in deepcopy(rows).items()}
            table_rows = []
            for _ in range(10):
                print(f"{_ + 1} time of {table}")
                row = create_table[table](**rows_list)
                session.add(row)
                table_rows.append(row)
            session.commit()

            for row in table_rows:
                session.refresh(row)
                rows[table].append(row)


if __name__ == "__main__":
    main()
