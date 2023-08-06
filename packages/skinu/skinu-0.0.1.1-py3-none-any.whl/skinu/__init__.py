

#
# Loggin methods
#

def configure_logging(p_enabled: bool):
    import logging
    from skinu._internal._logs import _skinuLog

    if p_enabled == True:
        _skinuLog.getLogger().setLevel(logging.DEBUG)
    else:
        _skinuLog.getLogger().setLevel(logging.CRITICAL)
