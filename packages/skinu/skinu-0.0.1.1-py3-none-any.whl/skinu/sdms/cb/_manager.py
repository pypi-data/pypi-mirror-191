import time
from datetime import timedelta

from couchbase.management.collections import (CollectionManager)
from couchbase.exceptions import InvalidArgumentException, BucketAlreadyExistsException, BucketDoesNotExistException, ScopeAlreadyExistsException, ScopeNotFoundException, CollectionAlreadyExistsException, CollectionNotFoundException, QueryIndexAlreadyExistsException, QueryIndexNotFoundException, InternalServerFailureException
from couchbase.management.buckets import (BucketType, ConflictResolutionType, CreateBucketSettings)
from couchbase.management.collections import (CollectionSpec)
from couchbase.management.options import (CreatePrimaryQueryIndexOptions, DropPrimaryQueryIndexOptions, CreateQueryIndexOptions, DropQueryIndexOptions)

from skinu._internal._logs import _skinuLog

import skinu.sdms as sdms


#
# class sdmsManager
#
class sdmsManager:
    #
    # private methods
    #

    @staticmethod
    def _retry(func, *args, back_off=0.5, limit=5, **kwargs) -> None:
        for i in range(limit):
            try:
                return func(*args, **kwargs)
            except Exception:
                _skinuLog.getLogger().info("Retry in {} seconds...".format((i + 1) * back_off))
                time.sleep((i + 1) * back_off)

        e = Exception("Unable to successfully receive result from {}".format(func))
        _skinuLog.getLogger().error(e)

        raise e

    @staticmethod
    def _get_scope(p_collection_mgr: CollectionManager, p_scope_name: str) -> None:
        return next((s for s in p_collection_mgr.get_all_scopes() if s.name == p_scope_name), None)

    @staticmethod
    def _get_collection(p_collection_mgr: CollectionManager, p_scope_name: str, p_collectio_name: str) -> None:
        tmp_scope = sdmsManager._get_scope(p_collection_mgr, p_scope_name)
        if tmp_scope:
            return next((c for c in tmp_scope.collections if c.name == p_collectio_name), None)

        return None

    #
    # bucket methods
    #

    @staticmethod
    def create_bucket(p_bucket_name: str, p_ram_quota_mb: int, p_num_replicas: int = 0, p_flush_enabled: bool = True) -> bool:
        tmp_ret = False

        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_bucket_manager = tmp_cb_cluster.buckets()

        tmp_bucket_settings = CreateBucketSettings(name=p_bucket_name,
                                                   flush_enabled=p_flush_enabled,
                                                   ram_quota_mb=p_ram_quota_mb,
                                                   num_replicas=p_num_replicas,
                                                   bucket_type=BucketType.COUCHBASE,
                                                   conflict_resolution_type=ConflictResolutionType.SEQUENCE_NUMBER)
        try:
            tmp_cb_bucket_manager.create_bucket(tmp_bucket_settings)
            tmp_ret = True
        except BucketAlreadyExistsException as baee:
            _skinuLog.getLogger().warning(baee)
            tmp_ret = False

        return tmp_ret

    @staticmethod
    def flush_bucket(p_bucket_name: str) -> bool:
        tmp_ret = False

        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_bucket_manager = tmp_cb_cluster.buckets()

        try:
            tmp_cb_bucket_manager.flush_bucket(p_bucket_name)
            tmp_ret = True
        except BucketDoesNotExistException as bdnee:
            _skinuLog.getLogger().warning(bdnee)
            tmp_ret = False

        return tmp_ret

    @staticmethod
    def drop_bucket(p_bucket_name: str) -> bool:
        tmp_ret = False

        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_bucket_manager = tmp_cb_cluster.buckets()

        try:
            tmp_cb_bucket_manager.drop_bucket(p_bucket_name)
            tmp_ret = True
        except BucketDoesNotExistException as bdnee:
            _skinuLog.getLogger().warning(bdnee)
            tmp_ret = False

        return tmp_ret

    @staticmethod
    def is_exist_bucket(p_bucket_name: str) -> bool:
        import skinu.sdms as sdms

        tmp_ret = False

        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_bucket_manager = tmp_cb_cluster.buckets()

        try:
            tmp_bucket = tmp_cb_bucket_manager.get_bucket(p_bucket_name)
            if tmp_bucket != None and tmp_bucket.name == p_bucket_name:
                tmp_ret = True
        except BucketDoesNotExistException as bdnee:
            _skinuLog.getLogger().warning(bdnee)
            tmp_ret = False

        return tmp_ret

    @staticmethod
    async def async_create_bucket(p_bucket_name: str, p_ram_quota_mb: int, p_num_replicas: int = 0, p_flush_enabled: bool = True) -> dict:
        tmp_ret = sdmsManager.create_bucket(p_bucket_name, p_ram_quota_mb, p_num_replicas, p_flush_enabled)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name}

    @staticmethod
    async def async_flush_bucket(p_bucket_name: str) -> dict:
        tmp_ret = sdmsManager.flush_bucket(p_bucket_name)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name}

    @staticmethod
    async def async_drop_bucket(p_bucket_name: str) -> dict:
        tmp_ret = sdmsManager.drop_bucket(p_bucket_name)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name}

    @staticmethod
    async def async_is_exist_bucket(p_bucket_name: str) -> dict:
        tmp_ret = sdmsManager.is_exist_bucket(p_bucket_name)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name}

    #
    # collection methods
    #

    @staticmethod
    def create_collection(p_bucket_name: str, p_scope_name: str, p_collection_name: str) -> bool:
        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_collection_manager = tmp_cb_cluster.bucket(p_bucket_name).collections()

        try:
            tmp_cb_collection_manager.create_scope(p_scope_name)
        except ScopeAlreadyExistsException as saee:
            _skinuLog.getLogger().warning(saee)
        except InternalServerFailureException as err:
            _skinuLog.getLogger().warning(err)

        try:
            sdmsManager._retry(sdmsManager._get_scope, tmp_cb_collection_manager, p_scope_name)
        except Exception as e:
            _skinuLog.getLogger().warning(e)

        try:
            tmp_cb_collection_spec = CollectionSpec(p_collection_name, scope_name=p_scope_name)
            tmp_cb_collection_manager.create_collection(tmp_cb_collection_spec)
        except CollectionAlreadyExistsException as caee:
            _skinuLog.getLogger().warning(caee)
            return False
        except InternalServerFailureException as err:
            _skinuLog.getLogger().warning(err)
            return False

        tmp_cb_collection = None
        try:
            tmp_cb_collection = sdmsManager._retry(sdmsManager._get_collection, tmp_cb_collection_manager, p_scope_name, p_collection_name)
        except Exception as e:
            _skinuLog.getLogger().warning(e)
            return False

        tmp_ret = True
        if tmp_cb_collection == None:
            tmp_ret = False

        return tmp_ret

    @staticmethod
    def drop_collection(p_bucket_name: str, p_scope_name: str, p_collection_name: str) -> bool:
        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_collection_manager = tmp_cb_cluster.bucket(p_bucket_name).collections()

        tmp_cb_collection_spec = CollectionSpec(p_collection_name, scope_name=p_scope_name)

        tmp_ret = True
        try:
            tmp_cb_collection_manager.drop_collection(tmp_cb_collection_spec)

        except ScopeNotFoundException as snfe:
            _skinuLog.getLogger().warning(snfe)
            tmp_ret = False

        except CollectionNotFoundException as cnfe:
            _skinuLog.getLogger().warning(cnfe)
            tmp_ret = False

        return tmp_ret

    @staticmethod
    def is_exist_collection(p_bucket_name: str, p_scope_name: str, p_collection_name: str) -> bool:
        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_collection_manager = tmp_cb_cluster.bucket(p_bucket_name).collections()

        tmp_collection = sdmsManager._get_collection(tmp_cb_collection_manager, p_scope_name, p_collection_name)
        if tmp_collection != None:
            return True

        return False

    @staticmethod
    async def async_create_collection(p_bucket_name: str, p_scope_name: str, p_collection_name: str) -> dict:
        tmp_ret = sdmsManager.create_collection(p_bucket_name, p_scope_name, p_collection_name)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name, "scope_name": p_scope_name, "collection_name": p_collection_name}

    @staticmethod
    async def async_drop_collection(p_bucket_name: str, p_scope_name: str, p_collection_name: str) -> dict:
        tmp_ret = sdmsManager.drop_collection(p_bucket_name, p_scope_name, p_collection_name)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name, "scope_name": p_scope_name, "collection_name": p_collection_name}

    @staticmethod
    async def async_is_exist_collection(p_bucket_name: str, p_scope_name: str, p_collection_name: str) -> dict:
        tmp_ret = sdmsManager.is_exist_collection(p_bucket_name, p_scope_name, p_collection_name)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name, "scope_name": p_scope_name, "collection_name": p_collection_name}

    #
    # primary index methods
    #

    @staticmethod
    def create_primary_index(p_bucket_name: str, p_scope_name: str, p_collection_name: str, p_index_name: str, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_query_indexes = tmp_cb_cluster.query_indexes()

        tmp_primary_query_index_option = CreatePrimaryQueryIndexOptions(index_name=p_index_name,
                                                                        num_replicas=p_num_replicas,
                                                                        ignore_if_exists=p_ignore_if_exists,
                                                                        scope_name=p_scope_name,
                                                                        collection_name=p_collection_name,
                                                                        timeout=p_timeout)

        tmp_ret = True
        try:
            tmp_cb_query_indexes.create_primary_index(p_bucket_name, tmp_primary_query_index_option)

        except InvalidArgumentException as iae:
            _skinuLog.getLogger().warning(iae)
            tmp_ret = False

        except QueryIndexAlreadyExistsException as qiaee:
            _skinuLog.getLogger().warning(qiaee)
            tmp_ret = False

        return tmp_ret

    @staticmethod
    def drop_primary_index(p_bucket_name: str, p_scope_name: str, p_collection_name: str, p_index_name: str, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_query_indexes = tmp_cb_cluster.query_indexes()

        tmp_primary_query_index_option = DropPrimaryQueryIndexOptions(index_name=p_index_name,
                                                                      ignore_if_exists=p_ignore_if_exists,
                                                                      scope_name=p_scope_name,
                                                                      collection_name=p_collection_name,
                                                                      timeout=p_timeout)

        tmp_ret = True
        try:
            tmp_cb_query_indexes.drop_primary_index(p_bucket_name, tmp_primary_query_index_option)
        except InvalidArgumentException as iae:
            _skinuLog.getLogger().warning(iae)
            tmp_ret = False

        except QueryIndexNotFoundException as qinfe:
            _skinuLog.getLogger().warning(qinfe)
            tmp_ret = False

        return tmp_ret

    @staticmethod
    async def async_create_primary_index(p_bucket_name: str, p_scope_name: str, p_collection_name: str, p_index_name: str, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_ret = sdmsManager.create_primary_index(p_bucket_name, p_scope_name, p_collection_name, p_index_name, p_num_replicas, p_ignore_if_exists, p_timeout)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name, "scope_name": p_scope_name, "collection_name": p_collection_name, "index_name": p_index_name}

    @staticmethod
    async def async_drop_primary_index(p_bucket_name: str, p_scope_name: str, p_collection_name: str, p_index_name: str, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_ret = sdmsManager.drop_primary_index(p_bucket_name, p_scope_name, p_collection_name, p_index_name, p_ignore_if_exists, p_timeout)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name, "scope_name": p_scope_name, "collection_name": p_collection_name, "index_name": p_index_name}

    #
    # index methods
    #

    def create_index(p_bucket_name: str, p_scope_name: str, p_collection_name: str, p_index_name: str, p_fields: list, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_query_indexes = tmp_cb_cluster.query_indexes()

        tmp_query_index_option = CreateQueryIndexOptions(num_replicas=p_num_replicas,
                                                         ignore_if_exists=p_ignore_if_exists,
                                                         scope_name=p_scope_name,
                                                         deferred=False,
                                                         collection_name=p_collection_name,
                                                         timeout=p_timeout)

        tmp_ret = True
        try:
            tmp_fields = ""
            for tmp_field in p_fields:
                tmp_fields += (", " if len(tmp_fields) > 0 else "") + "`" + tmp_field + "`"

            tmp_query = "CREATE INDEX `{}` ON `{}`.`{}`.`{}`({})".format(p_index_name, p_bucket_name, p_scope_name, p_collection_name, tmp_fields)
            tmp_cb_cluster.query(tmp_query).execute()
            # tmp_cb_query_indexes.create_index(p_bucket_name, index_name=p_index_name, fields=p_fields, options=tmp_query_index_option)

        except InvalidArgumentException as iae:
            _skinuLog.getLogger().warning(iae)
            tmp_ret = False

        except QueryIndexAlreadyExistsException as qiaee:
            _skinuLog.getLogger().warning(qiaee)
            tmp_ret = False

        return tmp_ret

    @staticmethod
    def drop_index(p_bucket_name: str, p_scope_name: str, p_collection_name: str, p_index_name: str, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_cb_cluster = sdms.sdms_get_cluster()
        tmp_cb_query_indexes = tmp_cb_cluster.query_indexes()

        tmp_query_index_option = DropQueryIndexOptions(ignore_if_exists=p_ignore_if_exists,
                                                       scope_name=p_scope_name,
                                                       collection_name=p_collection_name,
                                                       timeout=p_timeout)

        tmp_ret = True
        try:
            # tmp_cb_query_indexes.drop_index(p_bucket_name, p_index_name, options=tmp_query_index_option)
            tmp_query = "DROP INDEX `{}` ON `{}`.`{}`.`{}`".format(p_index_name, p_bucket_name, p_scope_name, p_collection_name)
            tmp_cb_cluster.query(tmp_query).execute()

        except InvalidArgumentException as iae:
            _skinuLog.getLogger().warning(iae)
            tmp_ret = False

        except QueryIndexNotFoundException as qinfe:
            _skinuLog.getLogger().warning(qinfe)
            tmp_ret = False

        return tmp_ret

    @staticmethod
    async def async_create_index(p_bucket_name: str, p_scope_name: str, p_collection_name: str, p_index_name: str, p_fields: list, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_ret = sdmsManager.create_index(p_bucket_name, p_scope_name, p_collection_name, p_index_name, p_fields, p_num_replicas, p_ignore_if_exists, p_timeout)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name, "scope_name": p_scope_name, "collection_name": p_collection_name, "index_name": p_index_name}

    @staticmethod
    async def async_drop_index(p_bucket_name: str, p_scope_name: str, p_collection_name: str, p_index_name: str, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_ret = sdmsManager.drop_index(p_bucket_name, p_scope_name, p_collection_name, p_index_name, p_ignore_if_exists, p_timeout)
        return {"is_success": tmp_ret, "bucket_name": p_bucket_name, "scope_name": p_scope_name, "collection_name": p_collection_name, "index_name": p_index_name}
