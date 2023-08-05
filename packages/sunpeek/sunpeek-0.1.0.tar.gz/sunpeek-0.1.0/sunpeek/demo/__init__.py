import os
import pathlib

DEMO_CONFIG_PATH = os.path.join(os.path.abspath(pathlib.Path(__file__).parent),
                                'plant_config_FHW_Arcon_South.json')
DEMO_DATA_PATH_2DAYS = os.path.join(os.path.abspath(pathlib.Path(__file__).parent),
                                    'FHW_collector_array_ArcS__2017-05-01__2017-05-02__1m.csv')
DEMO_DATA_PATH_1MONTH = os.path.join(os.path.abspath(pathlib.Path(__file__).parent),
                                     'FHW_collector_array_ArcS__2017-05-01__2017-05-31__1m.csv')
DEMO_DATA_PATH_1YEAR = os.path.join(os.path.abspath(pathlib.Path(__file__).parent),
                                    'FHW_collector_array_ArcS__2017-01-01__2017-12-31__1m.csv')
