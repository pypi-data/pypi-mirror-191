import json
import os
from sunpeek.common import utils
from sqlalchemy.orm import Session

from sunpeek.common import config_parser, crud, data_uploader
import sunpeek.components as cmp
import sunpeek.demo

def create_demoplant(session: Session, name: str = None):
    with open(sunpeek.demo.DEMO_CONFIG_PATH, 'r') as f:
        conf = json.load(f)

    if name is not None:
        conf['plant']['name'] = name

    config_parser.make_and_store_plant(conf, session)

    return crud.get_plants(session, plant_name=conf['plant']['name'])


def add_demo_data(plant: cmp.Plant, session: Session = None, tz: str = 'UTC'):
    if session is not None:
        up = data_uploader.DataUploader_db(plant=plant,
                                           files=[sunpeek.demo.DEMO_DATA_PATH_1MONTH],
                                           timezone=tz,
                                           session=session)
        up.do_upload()   # includes virtual sensor calculation
    else:
        plant.use_csv(csv_files=[fn], timezone=tz)    # includes virtual sensor calculation
