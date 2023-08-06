from datetime import timedelta

from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions
from couchbase.cluster import Cluster

from skinu.sdms import sdmsConfig


#
# class _skinuGlobal
#
class _skinuGlobal:
    __Config: sdmsConfig = None
    __Cluster: Cluster = None

    @staticmethod
    def init():
        _skinuGlobal.__Config = None
        _skinuGlobal.__Cluster = None

        # print("inner init skinu global")

    def init_config(p_mode: str) -> None:
        _skinuGlobal.__Config = sdmsConfig(p_mode)

    def init_cluster() -> None:
        auth = PasswordAuthenticator(_skinuGlobal.__Config.username, _skinuGlobal.__Config.password)
        options = ClusterOptions(auth)
        # options.apply_profile("wan_development")
        _skinuGlobal.__Cluster = Cluster("couchbase://{}".format(_skinuGlobal.__Config.endpoint), options)
        # _skinuGlobal.__Cluster.wait_until_ready(timedelta(seconds=_skinuGlobal.__Config.connection_timeout))

    def get_config() -> sdmsConfig:
        return _skinuGlobal.__Config

    def get_cluster() -> Cluster:
        return _skinuGlobal.__Cluster


#
# init
#
_skinuGlobal.init()
