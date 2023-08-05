import enum
from sunpeek.components.fluids import UninitialisedFluid
from sunpeek.components.types import UninitialisedCollectorType


class VerifyValidateMode(str, enum.Enum):
    validate = 'validate'
    verify = 'verify'


def assert_valid_collector(coll):
    assert coll is not None, 'Collector is None'
    assert not isinstance(coll, UninitialisedCollectorType), \
        'Collector is uninitialized, it is a "UninitialisedCollectorType"'


def assert_valid_fluid(fluid):
    assert fluid is not None
    assert not isinstance(fluid, UninitialisedFluid)