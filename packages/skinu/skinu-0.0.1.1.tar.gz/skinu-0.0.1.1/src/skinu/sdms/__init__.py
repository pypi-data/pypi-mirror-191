from skinu.sdms._config import sdmsConfig
from couchbase.cluster import Cluster


#
# __all__
#
__all__ = ["sdms_init", "sdms_get_config", "sdms_get_cluster", "sdmsConfig"]


def sdms_init(p_mode: str) -> None:
    from skinu._internal._global import _skinuGlobal
    from skinu._internal._logs import _skinuLog

    if _skinuGlobal.get_config() == None:
        _skinuGlobal.init_config(p_mode)
    else:
        e = Exception("already init sdms configuration !")
        _skinuLog.getLogger().critical(e)

        # 리눅스 상태에서 오류가 발생함 - (리눅스는 프로세스 방식이 아닌듯)
        # raise e


def sdms_get_config() -> sdmsConfig:
    from skinu._internal._global import _skinuGlobal
    from skinu._internal._logs import _skinuLog

    if _skinuGlobal.get_config() == None:
        e = Exception("sdms config initialize yet !")
        _skinuLog.getLogger().critical(e)

        raise e

    return _skinuGlobal.get_config()


def sdms_get_cluster() -> Cluster:
    from skinu._internal._global import _skinuGlobal
    from skinu._internal._logs import _skinuLog

    if _skinuGlobal.get_config() == None:
        e = Exception("sdms config initialize yet !")
        _skinuLog.getLogger().critical(e)

        raise e

    if _skinuGlobal.get_cluster() == None:
        _skinuGlobal.init_cluster()

    return _skinuGlobal.get_cluster()
