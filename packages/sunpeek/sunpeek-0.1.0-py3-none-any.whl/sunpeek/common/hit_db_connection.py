import asyncio
from io import BytesIO
import sys, os
import psycopg2
from psycopg2 import OperationalError, sql
import psycopg2.extras as extras
import pandas as pd
import time
import datetime
from sunpeek.common.utils import hit_logger


# default page size for database execute - this can be very large which should improve performance
DEFAULT_PAGE_SIZE = 100000


def show_psycopg2_exception(err):
    """Prints errors ocurred during postgresql db interactions.

    Parameters
    ----------
    err
        Error catched in program execution regarding PostgreSQL operations.

    Notes
    -----
    This code is part of the article by Learner CARES in 
    https://medium.com/analytics-vidhya/part-4-pandas-dataframe-to-postgresql-using-python-8ffdb0323c09
    Used for debugging and logging purposes.

    """
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occured
    line_n = traceback.tb_lineno
    hit_logger.error(f"\n[psycopg2_exception] ERROR: {err} on line number: {line_n}")
    hit_logger.error(f"[psycopg2_exception] traceback: {traceback} -- type: {err_type}")
    hit_logger.error(f"\n[psycopg2_exception] extensions.Diagnostics: {err.diag}")
    hit_logger.error(f"[psycopg2_exception] pgerror: {err.pgerror}")
    hit_logger.error(f"[psycopg2_exception] pgcode: {err.pgcode} \n")


# connection methods


def get_db_connection_dict():
    try:
        port = os.environ.get('HIT_DB_HOST', 'localhost:5432').split(':')[1]
    except IndexError:
        port = 5432

    conn_params_dict = {
        "host": os.environ.get('HIT_DB_HOST', 'localhost:5432').split(':')[0],
        "port": port,
        "database": os.environ.get('HIT_DB_NAME', 'harvestit'),
        "user": os.environ.get('HIT_DB_USER'),
        "password": os.environ.get('HIT_DB_PW')
    }

    return conn_params_dict


def get_db_connection():
    """Init db connections
    """
    db_connection = connect(get_db_connection_dict())
    if db_connection is None:
        raise ConnectionError('Failed to connect to to database')
    return db_connection


def connect(conn_params_dict):
    """Connects to an specific database.

    Parameters
    ----------
    conn_params_dict : `dict` 
        A dictionary containing the user credentials for the conection,
        the host and the name of the desired database.

    Returns
    -------
    connection : `psycopg2_connection`
        Established connection object to database.
    """
    # TODO del
    connection = None
    try:
        hit_logger.info('[connect] Connecting to the PostgreSQL...........')
        connection = psycopg2.connect(**conn_params_dict)
        # CONNECTION = "postgres://postgres:password@srv-tehs-02.aee2013.local:5432/hit"
        # connection = psycopg2.connect(CONNECTION)
        hit_logger.info("[connect] Connected !")

    except OperationalError as err:
        hit_logger.exception(err)
        # passing exception to function
        show_psycopg2_exception(err)
        # set the connection to 'None' in case of error
        connection = None
    return connection


def disconnect_db(connection):
    """Closes the connection with database.

    Parameters
    ----------
    connection : `psycopg2_connection`
        Connection object to database.
    """
    connection.close()
    hit_logger.info("[disconnect_db] HIT DB connection closed!")


# util methods
def db_table_exists(connection, table_name):
    """
    Checks the existence of the provided table in the database. Used for initialization of dynamic table creation.

    Parameters
    ----------
    connection : `psycopg2_connection`
        Connection object to database.

    table_name : `str`
        Table to search in between the tables in database.

    Returns
    -------
    True/False : `bool`
        True if table exists in database, False otherwise.
    """

    cursor = connection.cursor()
    query = f"""SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = '{table_name}');"""
    cursor.execute(query)
    # TODO nicen
    if cursor.fetchone()[0]:
        # if table exists
        return True
    else:
        return False


# GET


def get_table_columns(connection, table_name):
    """
    Retrieves a list of the table column names from the specified table.

    Parameters
    ----------
    connection : `psycopg2_connection`
        Connection object to database.
    
    table_name : `str`
        Name of the table to retrieves the columns from.

    Returns
    -------
    columns : `list`
        A list containing the column names of the specified table.

    """
    # declare an empty list for the column names
    columns = []

    # declare cursor objects from the connection
    col_cursor = connection.cursor()

    # concatenate string for query to get column names
    # SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'some_table';
    col_names_str = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE "
    col_names_str += "table_name = '{}';".format(table_name)

    try:
        sql_object = sql.SQL(
            """SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = {table_name}"""
            # pass SQL statement to sql.SQL() method
        ).format(
            # pass the identifier to the Identifier() method
            table_name=sql.Identifier(table_name)
        )

        # execute the SQL string to get list with col names in a tuple
        col_cursor.execute(sql_object)
        # get the tuple element from the liast
        col_names = (col_cursor.fetchall())
        # iterate list of tuples and grab first element
        for tup in col_names:
            # append the col name string to the list
            columns += [tup[0]]

        # close the cursor object to prevent memory leaks
        col_cursor.close()

    except Exception as err:
        hit_logger.exception(err)

    # return the list of column names
    return columns


def get_sensor_data(connection, sensor_names, table_name, start_timestamp, end_timestamp=None):
    """Retrieves the data from a sensor in the specified table. It can return both a single value or a range depending on the timestamps provided.
    
    Parameters
    ----------
    connection : `psycopg2_connection`
        Connection object to database.
    
    sensor_names : `str`, `list`
        Name of the sensor(s) to retrieve the data.
    
    table_name : `str`
        Name of the table where the sensor data is stored.

    start_timestamp,`datetime.datetime` or `str`
        Timestamp of the data entry.
    
    end_timestamp, optional `datetime.datetime` or `str`, optional
        Timestamp to retrieve a range of values if provided.
    
    """

    hit_logger.info(
        f"[get_sensor_data] Getting data for sensor \"{sensor_names}\" in \"{table_name}\" table")

    # SQL query to execute
    timestamp_col_name = "ds"
    if isinstance(sensor_names, str):
        sensor_names = [sensor_names]

    fields = [sql.Identifier(col.lower()) for col in sensor_names]
    fields = [sql.Identifier(timestamp_col_name)] + fields

    if end_timestamp:
        sql_object = sql.SQL(
            """SELECT {fields} FROM {tb_name} WHERE {col_name} BETWEEN {start_tmstmp} AND {end_tmstmp} ORDER BY {order_col_name} ASC"""
        ).format(
            fields=sql.SQL(',').join(fields),
            tb_name=sql.Identifier(table_name),
            col_name=sql.Identifier(timestamp_col_name),
            start_tmstmp=sql.Literal(start_timestamp),
            end_tmstmp=sql.Literal(end_timestamp),
            order_col_name=sql.Identifier(timestamp_col_name)
        )
    else:
        # TODO Does not work because sensor_names are list -> TypeError
        # query for queh just start timestamp is supplied
        sql_object = sql.SQL(
            """SELECT {fields} FROM {tb_name} WHERE {col_name} = {start_tmstmp} ORDER BY {order_col_name} ASC"""
        ).format(
            fields=sql.SQL(',').join([
                sql.Identifier(timestamp_col_name),
                sql.Identifier(sensor_names),
            ]),
            tb_name=sql.Identifier(table_name),
            col_name=sql.Identifier(timestamp_col_name),
            start_tmstmp=sql.Literal(start_timestamp),
            order_col_name=sql.Identifier(timestamp_col_name)
        )

    cursor = connection.cursor()
    try:
        t_start = time.time()
        cursor.execute(sql_object)
        hit_logger.info(f"[get_sensor_data] Data retrieved in {time.time()-t_start}")

        query_data = cursor.fetchall()
        sensor_data = pd.DataFrame(list(query_data), columns=['ds']+sensor_names)
        sensor_data = sensor_data.set_index('ds', drop=True)

        # close the cursor object to prevent memory leaks
        cursor.close()
        return sensor_data

    except (Exception, psycopg2.DatabaseError) as err:
        hit_logger.error("[get_sensor_data] Error in get_sensor_data()")
        # pass exception to function
        if isinstance(err, (psycopg2.DatabaseError, OperationalError)):
            show_psycopg2_exception(err)
        cursor.close()


# INSERT
# TODO no usages found. what is this?
def copy_from_dataFile(connection, uploaded_file, table_name):
    cursor = connection.cursor()
    try:
        file_io = BytesIO(uploaded_file.file.read())
        cursor.copy_from(file_io, table_name, sep=";")
        connection.commit()
        hit_logger.info(
            "[copy_from_dataFileData] inserted using copy_from_datafile() successfully....")
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        # pass exception to function
        hit_logger.error(
            f"[copy_from_dataFile] Failure to insert from file {uploaded_file.filename}")
        hit_logger.exception(error)
        show_psycopg2_exception(error)
        cursor.close()
        connection.rollback()



# TODO On psycopg2 bulk inserts
# https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
# fastest:

# def copy_from_stringio(conn, df, table):
#     """
#     Here we are going save the dataframe in memory
#     and use copy_from() to copy it to the table
#     """
#     # save dataframe to an in memory buffer
#     buffer = StringIO()
#     df.to_csv(buffer, index_label='id', header=False)
#     buffer.seek(0)
#
#     cursor = conn.cursor()
#     try:
#         cursor.copy_from(buffer, table, sep=",")
#         conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("Error: %s" % error)
#         conn.rollback()
#         cursor.close()
#         return 1
#     print("copy_from_stringio() done")
#     cursor.close()



# TODO faster? https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
# psycopg2.extras.execute_values (
#     cursor, insert_query, data, template=None, page_size=100
# )


# TODO rename insert_dataframe
def execute_batch(connection,
                  datafrm,
                  table,
                  page_size=DEFAULT_PAGE_SIZE):

    """

    Should batch-erase overlapping data.
    See data_uploader._post_upload:
                hit_db.delete_overlapping_data(self.db_connection, self.table_name,
                                           overlapping_boundaries=(df.index[0], df.index[-1]))


    """

    start_t = time.time()
    hit_logger.info(f"[execute_batch] Inserting data into \"{table}\" table")
    # TODO Move to Context. This is managed by Context.use_dataframe
    if datafrm.index.name == 'ds':
        datafrm = datafrm.reset_index()
    assert 'ds' in datafrm.columns
    try:
        assert datafrm.ds.dt.tz is not None, 'Data must have a timezone aware datetime column or index called "ds".'
    except AttributeError:
        raise AttributeError('Data must have a datetime index or column called "ds".')

    # if datafrm.index.name != 'ds':
    #     datafrm.set_index('ds', drop=True, inplace=True)

    # TODO Normal format: Must have DatetimeIndex, tz aware. Make it a 'ds' column
    # from common.utils import validate_timezone
    # ...
    # df = df.rename_axis('ds').reset_index()

    # We dont need to store units. We store everything as float64, units are attached by Context class

    # Creating a list of tupples from the dataframe values
    # list(df.itertuples(index=False, name=None))
    # TODO Improve performance. Tuple comprehension is the slowest according to
    # https://stackoverflow.com/questions/9758450/pandas-convert-dataframe-to-array-of-tuples
    # df.to_records(index=False).tolist()
    # s_time = time.time()
    # datafrm.columns = [name.lower() for name in datafrm.columns]
    # datafrm.to_sql(table, db_engine, if_exists='append')
    # print(f"batch insert done in: {time.time() - s_time}")
    # return True
    tpls = [tuple(x) for x in datafrm.to_numpy()]
    hit_logger.info(f"[execute_batch] Tuple to save example:\n{tpls[0]}")

    # SQL query to execute
    s_time = time.time()
    insert_flds = [fld_name.lower().strip() for fld_name in datafrm.columns]
    insert_str = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table),
        sql.SQL(",").join(map(sql.Identifier, insert_flds)),
        sql.SQL(",").join(sql.Placeholder() * len(insert_flds))
    )
    print(f"insert stament creation done in: {time.time() - s_time}")
    # insert_str = sql.SQL("INSERT INTO {} ({}) VALUES {}").format(
    #     sql.Identifier(table),
    #     sql.SQL(",").join(map(sql.Identifier, insert_flds)),
    #     sql.Placeholder()
    # )

    cursor = connection.cursor()
    try:
        s_time = time.time()
        # extras.execute_batch(cursor, insert_str, tpls, page_size)
        cursor.executemany(insert_str, tpls)
        print(f"batch insert done in: {time.time() - s_time}")
        # extras.execute_values(cursor, insert_str, tpls)
        # perhaps: cursor.execute(insert_str, tpls, page_size=page_size)
        hit_logger.info(f"[execute_batch] Committed data insertion successfully in {time.time()-start_t} seconds.")
        return True
        # TODO Consider using executemany()
        # tuples = [tuple(x) for x in df.to_numpy()]
        # # Comma-separated dataframe columns
        # cols = ','.join(list(df.columns))
        # # SQL quert to execute
        # query  = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s)" % (table, cols)
        # cursor = conn.cursor()
        # try:
        #     cursor.executemany(query, tuples)
        #     conn.commit()
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print("Error: %s" % error)
        #     conn.rollback()
        #     cursor.close()
        #     return 1
        # print("execute_many() done")
        # cursor.close()

    except (Exception, psycopg2.DatabaseError) as err:
        hit_logger.error("[execute_batch] Error in execute_batch()")
        hit_logger.exception(err)
        # pass exception to function
        if isinstance(err, (psycopg2.DatabaseError, OperationalError)):
            show_psycopg2_exception(err)
        cursor.close()
        connection.rollback()
        return False


# UPDATE

# TODO rename, align with execute batch, insert_series
def update_virtual_sensor_data(connection,
                               sensor_data: pd.Series,
                               table,
                               # plant_name: str,
                               # sensor_raw_name: str,
                               page_size=DEFAULT_PAGE_SIZE):

    """Saves the re calculated data of a virtual sensor in the corresponsing raw_table.

    Is different from execute_batch() in that it does not batch-erase overlapping data

    """

    hit_logger.info(f"[update_virtual_sensor_data] Inserting data into \"{table}\" table")
    # hit_logger.info("[save_virtual_sensor_data] Saving...")

    # # table_name = f"raw_data_{plant_name.replace(' ', '_').lower()}"
    # units = []
    # tpls = []
    # for timestamp_index, pint_value in sensor_data.items():
    #     tpls.append((pint_value.magnitude, timestamp_index))
    #     units.append(pint_value.units)

    # We dont need to store units. We store everything as float64, units are attached by Context class

    # df = sensor_data.reset_index()
    # df.to_records(index=False).tolist()
    # Make sure 'ds' timestamp columns
    # tpls = sensor_data.reset_index().to_records().tolist()
    # sensor_data
    fld_name = sensor_data.name
    # tpls = [tuple(x) for x in sensor_data.to_numpy()]
    df = sensor_data.to_frame()
    df = df.rename_axis('ds').reset_index()
    df = df.reindex(columns=df.columns[::-1])
    tpls = df.to_records(index=False).tolist()
    print(tpls[0])
    hit_logger.info(f"[execute_batch] Tuple to save example:\n{tpls[0]}")

    # insert_flds = [fld_name.lower().strip() for fld_name in sensor_data.name]
    # insert_flds = df.columns.to_list()

    # TODO BUG use upsert operation instead: https://wiki.postgresql.org/wiki/UPSERT
    # https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-upsert/
    # https://www.psycopg.org/docs/usage.html
    # This code adds number of sensor_data rows to the database

    # original
    insert_str = sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
        sql.Identifier(table),
        sql.Identifier(fld_name),
        sql.Placeholder(),
        sql.Identifier("ds"),
        sql.Placeholder()
    )
    # insert_str = sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
    #     sql.Identifier(table),
    #     sql.Identifier(sensor_data.columns[1]),
    #     sql.Placeholder(sensor_data.iloc[:,1]),
    #     sql.Identifier("ds"),
    #     sql.Placeholder(sensor_data.iloc[:,0])
    # )
    # https://stackoverflow.com/questions/60845779/psycopg2-how-to-insert-and-update-on-conflict-using-psycopg2-with-python
    # insert_sql = '''
    #     INSERT INTO tablename (col1, col2, col3, col4)
    #     VALUES (%s, %s, %s, %s)
    #     ON CONFLICT (col1) DO UPDATE SET
    #     (col2, col3, col4) = (EXCLUDED.col2, EXCLUDED.col3, EXCLUDED.col4);
    # '''

    cursor = connection.cursor()

    # cursor.rowcount
    # cursor.execute("""
    #     UPDATE table_name
    #     SET z = codelist.z
    #     FROM codelist
    #     WHERE codelist.id = vehicle.id;
    #     """)
    # cursor.rowcount

    try:
        extras.execute_batch(cursor, insert_str, tpls, page_size=page_size)
        # perhaps: cursor.execute(insert_str, tpls)
        hit_logger.info("[save_virtual_sensor_data] Virtual sensor data inserted successfully!")
        connection.commit()
        return True
    except (Exception, psycopg2.DatabaseError, OperationalError) as err:
        hit_logger.error(f"[save_virtual_sensor_data] Error in save_virtual_sensor_data()")
        hit_logger.exception(err)
        # pass exception to function
        if isinstance(err, (psycopg2.DatabaseError, OperationalError)):
            show_psycopg2_exception(err)
        cursor.close()
        connection.rollback()
        return False


def create_table_dynamic(connection, table_name, data_dict):
    """
    Creates a table dynamically based on the keys and datatypes from the provided dictionary

    Params
    ------
    `psycopg2_connection` connection: Connection object to database.
    `str` table_name: A string to name the db table.
    `dict` data_dict: Dictionary containing all the data to save.
    """

    hit_logger.info(f"[create_table_dynamic] Creating table {table_name} dynamically...")
    try:
        tipes_dict = {int: 'INTEGER',
                      float: 'NUMERIC (15,5)', str: 'VARCHAR(55)', datetime.datetime: 'TIMESTAMPTZ'}
        sql_types = []

        for key, value in data_dict.items():
            db_key = key.strip()
            work_value = value[0] if type(value) == dict else value

            # exchange types
            if type(work_value) == list:
                # analize first value since its a list (same types stored supposition)
                dt_col = None
                if "ds" in db_key:
                    var_type = f"{db_key} {tipes_dict[datetime.datetime]} UNIQUE INITIALLY DEFERRED"
                    # var_type = f"{db_key} {tipes_dict[datetime.datetime]}"
                    dt_col = 'ds'
                else:
                    var_type = f"{db_key} {tipes_dict[type(work_value[0])]}"
            else:
                if "ds" in db_key:
                    var_type = f"{db_key} {tipes_dict[datetime.datetime]} UNIQUE INITIALLY DEFERRED"
                    # var_type = f"{db_key} {tipes_dict[datetime.datetime]}"
                    dt_col = 'ds'
                else:
                    var_type = f"{db_key} {tipes_dict[type(work_value)]}"
            sql_types.append(var_type)

        types_str = ','.join(sql_types)
        create_query = f"CREATE TABLE {table_name} ({types_str}) WITH (fillfactor = 70)"

        # table creation
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        cursor.execute(create_query)
        mk_hypertable_query = f"SELECT create_hypertable('{table_name}', 'ds', chunk_time_interval => INTERVAL '1 month');"
        cursor.execute(mk_hypertable_query)
        hit_logger.info(f"[CTD] Table {table_name} created!")
        connection.commit()
        cursor.close()

    except OperationalError as err:
        # pass exception to function
        show_psycopg2_exception(err)
        hit_logger.exception(err)
        cursor.close()  #
        connection.rollback()


# DELETE

def delete_overlapping_data(connection, table_name, overlapping_boundaries):
    """
    Deletes all the entries in the DB in case there is overlapping with the incoming data.
    
    Returns
    -------
    overlapping : Bool
        Either overlapping entries were deleted in the db or not.
    """

    # overlaping handling
    # 1. Run delete command on database for entries inside the overlapping range
    # 2. This returns the number of rows affected, 0 if no entries are inside the range
    # 3. Return a boolean value reporting if the overlapping delete was carried out.

    overlapping = False
    left_boundary, right_boundary = overlapping_boundaries

    cursor = connection.cursor()
    rows_deleted = 0
    try:

        delete_str = sql.SQL("DELETE FROM {} WHERE {} BETWEEN {} AND {}").format(
            sql.Identifier(table_name),
            sql.Identifier("ds"),
            sql.Literal(left_boundary),
            sql.Literal(right_boundary)
        )

        cursor.execute(delete_str)
        rows_deleted = cursor.rowcount

        if rows_deleted > 0:
            hit_logger.warning(
                f"[delete_overlapping_data] Overlapping detected! Deleting data between the range [{left_boundary}, {right_boundary}] in the {table_name} table")
            hit_logger.warning(f"[delete_overlapping_data] Deleted overlapping entries: {rows_deleted}")
            overlapping = True
            return overlapping
        else:
            hit_logger.info(f"[delete_overlapping_data] The incoming data does not overlap with records in the db.")
            return overlapping

    except (Exception, psycopg2.DatabaseError, OperationalError) as err:
        hit_logger.exception(err)
        # pass exception to function
        if isinstance(err, (psycopg2.DatabaseError, OperationalError)):
            show_psycopg2_exception(err)
        cursor.close()
        connection.rollback()
        return False


# def data_property(connection_params_dict):
#     """
#     DEBUG METHOD, used only to simulate the step function calls as if they were inside te object factor from Sensor data property.
#
#     TODO
#     ----
#     Remove for main branch after testing with DB data
#     """
#     loop = asyncio.get_event_loop()
#     db_conn_coroutine = connect(connection_params_dict)
#     db_connection = loop.run_until_complete(db_conn_coroutine)
#
#     sensor_data_coroutine = get_sensor_data(db_connection, "shp1_body_temperature", "raw_data",
#                                             "2019-10-14 00:00:03+02", "2019-10-14 00:00:19+02")
#
#     sensor_data_dict = loop.run_until_complete(sensor_data_coroutine)
#     db_disconnect_routine = disconnect_db(db_connection)
#     loop.run_until_complete(db_disconnect_routine)


# if __name__ == "__main__":
#     start_time = time.time()
#
#     conn_params_dict = {
#         "host": "srv-tehs-02.aee2013.local",
#         "port": "5432",
#         "database": "hit",
#         "user": "postgres",
#         "password": "password"
#     }
#
#     data_property(conn_params_dict)
#
#     print("--- program finished after %s seconds ---" %
#           (time.time() - start_time))

def copy_upload(connection, datafrm, table):
    cursor = connection.cursor()
    try:
        fio = BytesIO()
        datafrm.to_csv(fio, sep=';', header=False)
        fio.seek(0)
        cursor.copy_from(fio, table, sep=';', null='', columns=[datafrm.index.name]+[col.lower() for col in datafrm.columns])
        cursor.close()
        return True
    except Exception as ex:
        hit_logger.error(ex)
        cursor.close()
        return False