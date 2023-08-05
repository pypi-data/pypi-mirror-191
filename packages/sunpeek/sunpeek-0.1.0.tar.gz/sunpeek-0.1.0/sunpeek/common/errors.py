class HitError(Exception):
    pass


class ConfigurationError(HitError):
    pass


class CollectorDefinitionError(HitError):
    """Error in CollectorType definition.
    E.g. if supplied information is contradictory or not sufficient for full CollectorType definition.
    See #70 for valid CollectorType definitions.
    """
    pass


class IncompatibleUnitError(HitError):
    """Supplied unit (of raw sensor) is not compatible with the expected unit, e.g. as defined in SensorType.
    """
    pass


class VirtualSensorConfigurationError(HitError):
    """Error in calcluation of virtual sensor due to missing input or input being None.
    """
    pass


class VirtualSensorCalculationError(HitError):
    """General error in definition / handling of virtual senso.
    """
    pass


class DuplicateNameError(HitError):
    """Error due to creating a component with a duplicate name, where this is not allowed"""
    pass


class SensorNotFoundError(HitError):
    """Error due to not finding a sensor when one was expected to exist"""
    pass

