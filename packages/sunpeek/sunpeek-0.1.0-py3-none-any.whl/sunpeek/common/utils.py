import logging
import os
import pathlib
import subprocess
import sys
# from io import BytesIO
import dotenv
import pandas as pd
import sqlalchemy.orm
from pydantic import BaseModel
from logging.config import dictConfig

from sunpeek.common.unit_uncertainty import to_s

dotenv.load_dotenv()

ROOT_DIR = os.path.abspath(pathlib.Path(__file__).parent.parent)
log_dir = os.path.join(ROOT_DIR, 'logs')
log_fname = os.path.join(log_dir, 'server.log')

API_LOCAL_BASE_URL = "http://127.0.0.1:8000/"
API_TOKEN = "harvestIT"


# async def handle_fhw_csv_data(csv_file, timezone):
#     print(f"[handle_fhw_csv_data] Handling FHW file: {csv_file.filename} ")
#     # skip row 1 since its a fixed index extra row
#
#     csv_buffer = BytesIO(csv_file.file.read())
#     csv_df = pd.read_csv(csv_buffer, sep=";", thousands=".", encoding='latin-1', skiprows=lambda x: x in [0, 2],
#                          decimal=",")
#     csv_df.rename(columns={csv_df.columns[0]: "Datuhr_timestamp", csv_df.columns[1]: "Fehlerzaehler"}, inplace=True)
#     # Add timezone info
#     csv_df['Datuhr_timestamp'] = csv_df['Datuhr_timestamp'].apply(lambda x: f"{x} {timezone}")
#     csv_buffer.seek(0)
#     #  save sensor units
#     units_df = pd.read_csv(csv_buffer, sep=";", thousands=".", encoding='latin-1', skiprows=1, nrows=1)
#     units_df = units_df.drop(units_df.columns[[0, 1]], axis=1)
#     units_df = units_df.rename(index={0: "sensor_unit"})
#     units_df = units_df.T.reset_index()
#     units_df = units_df.rename(columns={"index": "sensor_name"})
#     # powerful df function to apply to the whole df with a lambda expression, elementwise
#     units_df = units_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
#     # units_df['sensor_name'] = units_df['sensor_name'].apply(lambda x: x.strip())
#     # harcoded just for this use case
#     units_df["plant_id"] = "fhw"
#     print(f"[handle_fhw_csv_data] Units df:\n{units_df}")
#
#     return units_df, csv_df


async def handle_api_exceptions(caller: str, error_message: str, exception):
    print(f"[handle_api_exceptions] /!\\ An exception ocurred in {caller}. Preparing API and LOG entries...")

    err_type, err_obj, traceback = sys.exc_info()

    # details_dict = {"error_message": error_message, "exception_info": exception.}


class MissingEnvVar(Exception):
    def __init__(self, key):
        super().__init__("Value not found. This information should be stored in env variable " +
                         key + ". use: os.environ['" + key + "'] = <values>")


class LogConfig(BaseModel):
    """
    Logging configuration to be set for the server.

    Notes
    -----
    Modified code snipped originally by "Yash Nag" taken from:
    https://stackoverflow.com/questions/63510041/adding-python-logging-to-fastapi-endpoints-hosted-on-docker-doesnt-display-api

    """

    # LOGGER_NAME: str = "hit_logger"
    FILE_LOG_FORMAT: str = "|%(asctime)s| [%(levelname)s -> %(module)s] : %(message)s"
    STD_OUT_LOG_FORMAT: str = "%(levelprefix)s |%(asctime)s| %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Create log directory if it does not exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "std_out": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": STD_OUT_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "file_out": {
            "format": FILE_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    }
    handlers = {
        "default": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "formatter": "file_out",
            "class": "logging.FileHandler",
            "level": "WARNING",
            "filename": log_fname
        }
    }
    loggers = {
        "hit_logger": {"handlers": ["default", "file"], "level": LOG_LEVEL},
    }


def get_env(name):
    try:
        value = os.environ[name]
    except KeyError:
        raise MissingEnvVar(name)
    return value


def get_git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()


def get_git_branch():
    return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf').strip()


def get_commit_short_hash() -> str:
    try:
        with open(ROOT_DIR + '/.revision') as f:
            return f.readlines()[0]
    except (KeyError, FileNotFoundError):
        return 'unknown'


def get_commit_branch():
    try:
        with open(ROOT_DIR + '/.branch') as f:
            return f.readlines()[0]
    except (KeyError, FileNotFoundError):
        return 'unknown'


def get_db_conection_string():
    db_type = os.environ.get('HIT_DB_TYPE', 'postgresql')
    host = os.environ.get('HIT_DB_HOST', 'localhost:5432')
    user = os.environ.get('HIT_DB_USER')
    pw = os.environ.get('HIT_DB_PW')
    db_name = os.environ.get('HIT_DB_NAME', 'harvestit')
    dialects = {'postgresql': 'postgresql+psycopg2'}

    db_str = '{}://'.format(dialects[db_type])
    if user is not None:
        db_str = db_str + user
    if pw is not None:
        db_str = db_str + ':{}@'.format(pw)
    db_str = db_str + '{}/{}'.format(host.strip('/'), db_name)
    return db_str


def to_rd(*args):
    """Converts numeric inputs to pd.Series with pint dtype W/m².
    Useful to return radiation converter results.
    """
    out = *(None if elem is None else to_s(elem, unit_str='W m**-2') for elem in args),
    out = out[0] if len(out) == 1 else out
    return out


def validate_timezone(idx: pd.DatetimeIndex, timezone: str) -> pd.DataFrame:
    """Validates timezone information, trying to match DataFrame timezone and timezone string.

    Parameters
    ----------
    idx : pd.DatetimeIndex
    timezone : timezone string, example 'Europe/Berlin' or 'UTC'

    Returns
    -------
    idx : pd.DatetimeIndex, timezone-aware index

    Raises
    ------
    ValueError

    Notes
    -----
    Here is how all combinations are handled:
    1. No timezone in df, but timezone string given: ok
    2. Timezone in df, and no timezone string given: ok
    3. No timezone in df, and no timezone string given: error (timezone info is missing)
    4. Timezone both in df and as timezone string: error (because it's hard to check compatibility between a
    dynamically-offset string-based timezone like 'Europe/Vienna' with a FixedOffset timezone info that is the
    result of parsing timezone-aware timestamps).
    See also: https://pvlib-python.readthedocs.io/en/v0.3.0/timetimezones.html
    """

    hit_logger.info("[validate_timezone] Started. Checking for timezone consistency...")

    assert isinstance(idx, pd.DatetimeIndex), \
        'Input index expected to be a pandas DatetimeIndex.'
    tz_idx_none = idx.tzinfo is None

    if (timezone is None) and tz_idx_none:
        # No timezone information available at all -> error
        raise ValueError(
            'No timezone information found: Timezone string is None, '
            'and no timezone information was found in the provided pandas index.')

    if (timezone is not None) and not tz_idx_none:
        # Both timezone informations available -> error (see docstring)
        raise ValueError(
            'Ambiguous timezone information found: A timezone string (resulting in a dynamic offset) is given, '
            'and timezone information is also given in the pandas index (fixed offset).'
            'These two pieces of timezone information are incompatible. Use only one of them, string or pandas index.')

    if tz_idx_none:
        idx = idx.tz_localize(timezone, ambiguous='NaT', nonexistent='NaT')

    # If df.index is already timezone-aware, we can just simply return it
    return idx


db_engine = sqlalchemy.create_engine(get_db_conection_string(), pool_pre_ping=True)
S = sqlalchemy.orm.sessionmaker(db_engine)

# logger
dictConfig(LogConfig().dict())
hit_logger = logging.getLogger("hit_logger")
