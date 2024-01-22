from copy import deepcopy
from tqdm import tqdm
from bda_nesprisa.tables.types import TableName, table_names
from bda_nesprisa.tables import create_rows

# We use the SQLModel ORM since it is a superset of SQLAlchemy and it is design to work with FastAPI, which
# would make the work of typing an API way easier if we wanted to make a REST API for interacting with this data source
from sqlmodel import Session, create_engine

# Connection string for our Oracle DB
ENGINE_STRING = "oracle+oracledb://CDA14:BDA@oralabos.dsic.upv.es:1521/labora"

# Dict to keep track of the rows we have inserted into each table
# and be able to pass them as dependencies to create rows for other tables
rows: dict[TableName, list] = {table: [] for table in table_names}


# Main function, we pass the engine as a parameter so we can mock it in possible tests
def main(engine=create_engine(ENGINE_STRING)):
    # We use the Session context manager to avoid having to close the session manually
    # and the tqdm context manager to show a total progress bar
    with Session(engine, expire_on_commit=False) as session, tqdm(
        total=sum(table["num_rows"] for table in create_rows.values()), desc="Total"
    ) as pbar:
        try:
            # Iterate over each table and show a second progress bar for tables
            for table in tqdm(table_names, desc="Tables"):
                tqdm.write(f"--- Importing data into {table} table ---")

                # Create a copy of the rows dict and pass it to the create_rows function to inject possible dependencies
                rows_list = {f"{k}_list": v for k, v in deepcopy(rows).items()}

                # Get the number of rows to create for this table
                num_rows = create_rows[table]["num_rows"]

                # Call the create_rows function for this table and pass the rows_list dict as kwargs
                table_rows = create_rows[table]["fn"](
                    **rows_list, num_rows=num_rows, pbar=pbar
                )

                # Add the rows to the session
                for row in table_rows:
                    session.add(row)
                
                session.commit()
                
                for row in table_rows:
                    session.refresh(row)
                    
                rows[table].extend(table_rows)
                
        except Exception as e:
            session.rollback()
            raise e


if __name__ == "__main__":
    main()
