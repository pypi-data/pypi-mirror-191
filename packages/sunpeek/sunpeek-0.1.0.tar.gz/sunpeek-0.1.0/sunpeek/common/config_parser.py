import copy
import sunpeek.components as cmp
from sunpeek.common.errors import ConfigurationError


def make_full_plant(conf, session=None):
    conf = copy.deepcopy(conf)
    collector_types = {}
    if 'collector_types' in conf:
        col_types = conf['collector_types']
        for col_type in col_types:
            test_type = col_type.pop('test_type')
            if test_type in ['SST', "static"]:
                type_obj = cmp.CollectorTypeSST(**col_type)
            elif test_type in ['QDT', "dynamic"]:
                type_obj = cmp.CollectorTypeQDT(**col_type)
            else:
                raise ConfigurationError("CollectorType test_type parameter must be one of 'SST', 'static', 'QDT' or 'dynamic'")
            collector_types[type_obj.name] = type_obj
    if 'plant' in conf:
        conf = conf['plant']
        for array in conf['arrays']:
            if array['collector_type'] in collector_types.keys():
                array['collector_type'] = collector_types[array['collector_type']]

    plant = cmp.Plant(**conf)

    if session is not None:
        session.add(plant)
        session.rollback()

    return plant


def make_and_store_plant(conf, session):
    p = make_full_plant(conf, session)
    session.add(p)
    # done at each plant update anyway
    # p.config_virtuals()  # To ensure that sensor types, fluids etc. are available, do this after adding plant to session
    session.commit()
    return p
