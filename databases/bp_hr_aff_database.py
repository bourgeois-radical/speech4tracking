from sqlite3 import Error, connect, version
from pathlib import Path
import databases.constant_queries
from typing import List, Tuple

class BpHrAffectDatabase:

    def __init__(self):
        # TODO:
        #  if provided_p_value is None:
        #     self.specified_p_value = parameters.PREDEFINED_P_VALUE
        #  else:
        #     self.specified_p_value = provided_p_value

        # TODO: or should I provide them with the class initialization? Do we need this flexibility
        self.create_bp_hr_aff_table_query = databases.constant_queries.CREATE_BP_HR_AFF_TABLE
        self.insert_row_to_bp_hr_aff_query = databases.constant_queries.INSERT_ROW_TO_BP_HR_AFF
        self.create_demo_bp_hr_aff_db_query = databases.constant_queries.CREATE_DEMO_BP_HR_AFF_DB
        self.initialize_fake_measurements_in_demo_bp_hr_aff_query = \
            databases.constant_queries.INITIALIZE_FAKE_MEASUREMENTS_IN_DEMO_BP_HR_AFF_TABLE

    def create_connection(self, db_path: str):
        """Create a database connection to a SQLite database"""

        db_path = Path(db_path)

        connection = None
        try:
            connection = connect(db_path)
        except Error as error:
            print(error)

        return connection

    def create_table(self, connection):
        """Create a table from the create_table_query statement"""

        try:
            cursor = connection.cursor()
            cursor.execute(self.create_bp_hr_aff_table_query)
            connection.commit()
        except Error as error:
            print(error)

        return  # actually, returns None. It's a procedure in normal programming languages

    def insert_row(self, connection, systolic, diastolic, heart_rate, affect):
        """Insert a row with sys and dia pressure as well as heart rate and affect"""

        row_to_insert = (systolic, diastolic, heart_rate, affect)
        cursor = connection.cursor()
        cursor.execute(self.insert_row_to_bp_hr_aff_query, row_to_insert)
        connection.commit()

        return  # actually, returns None. It's a procedure in normal programming languages

    def close_connection(self, connection):

        connection.close()

        return  # actually, returns None. It's a procedure in normal programming languages

    def create_demo_connection(self, db_path: str):
        """This database if for demonstration purposes only"""

        db_path = Path(db_path)

        # create a demo db
        connection = None
        try:
            connection = connect(db_path)
        except Error as error:
            print(error)

        return connection

    def initialize_fake_measurements(self, connection):

        # create a table for fake measurements
        try:
            cursor = connection.cursor()
            cursor.execute(self.create_demo_bp_hr_aff_db_query)
            connection.commit()
        except Error as error:
            print(error)

        # initialize fake measurements inside the demo db
        try:
            cursor = connection.cursor()
            cursor.execute(self.initialize_fake_measurements_in_demo_bp_hr_aff_query)
            connection.commit()
        except Error as error:
            print(error)

        print('the demo table has been successfully created!')

        return  # actually, returns None. It's a procedure in normal programming languages

    def retrieve_measurements_for_demo_test(self, connection, rate_of_interest: str, affected_by: str) -> \
            List[Tuple[int, str, int, int, int, str]]:

        cursor = connection.cursor()
        cursor.execute(f"SELECT {rate_of_interest} FROM demo_bp_hr_aff WHERE affect='{affected_by}'")
        rows = cursor.fetchall()

        # print(f'the retrieved rows are of type {type(rows)}')
        # for row in rows:
        #     print(f'one row is of type {type(row)}')
        #     print(row)

        return rows





# if __name__ == '__main__':
#     path = input(r'Enter the path and the name of the databases you wanna create:')
#     create_connection(path)



