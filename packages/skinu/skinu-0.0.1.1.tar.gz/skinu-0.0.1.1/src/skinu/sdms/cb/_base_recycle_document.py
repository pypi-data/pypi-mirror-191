import copy
from datetime import timedelta
from abc import *

from couchbase.collection import Collection
from couchbase.options import QueryOptions
from couchbase.result import QueryResult

import pandas as pd

from skinu.core import dict_utils
from skinu._internal._logs import _skinuLog

import skinu.sdms as sdms
from skinu.sdms.cb import sdmsManager
from skinu.sdms.cb import sdmsN1ql
from skinu.sdms.cb._base_document import sdmsBaseDocument


#
# class sdmsBaseRecycleDocument
#
class sdmsBaseRecycleDocument(sdmsBaseDocument, metaclass=ABCMeta):
    def __init__(self,
                 p_cb_bucket_name: str,
                 p_cb_scope_name: str,
                 p_cb_collection_name: str,
                 p_cb_recycle_collection_name: str,
                 p_cb_document_name: str,
                 p_site_id: str,
                 p_meta_field_dict: dict,
                 p_meta_version: int,
                 p_meta_document_info_dict: dict,
                 p_is_exist_update_time_field: bool = True):
        super().__init__(
            p_cb_bucket_name,
            p_cb_scope_name,
            p_cb_collection_name,
            p_cb_document_name,
            p_site_id,
            p_meta_field_dict,
            p_meta_version,
            p_meta_document_info_dict,
            p_is_exist_update_time_field
        )

        self.__cb_recycle_collection_name = p_cb_recycle_collection_name

    #
    # abstract method 관련
    #

    def _request_upgrade_meta(self, p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        self._request_upgrade_meta_data(p_cb_collection, p_data_dict, p_meta_verion, p_document_version)

    @abstractmethod
    def _request_upgrade_meta_data(self, p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        nie = NotImplementedError("not implemented _request_upgrade_meta_data method")
        _skinuLog.getLogger().critical(nie)
        raise nie

    #
    # get (couchbase 관련)
    #

    def get_cb_collection_name(self, p_is_recycle: bool = False) -> str:
        return super()._get_cb_collection_name() if p_is_recycle == False else self.__cb_recycle_collection_name

    def get_cb_table_name(self, p_is_recycle: bool = False) -> str:
        return "`{0}`.`{1}`.`{2}`".format(super().get_cb_bucket_name(), super().get_cb_scope_name(), self.get_cb_collection_name(p_is_recycle))

    def get_cb_collection(self, p_is_recycle: bool = False) -> Collection:
        return sdms.sdms_get_cluster().bucket(super().get_cb_bucket_name()).scope(super().get_cb_scope_name()).collection(self.get_cb_collection_name(p_is_recycle))

    #
    # manager
    #

    def create_cb_collection(self, p_is_recycle: bool = False) -> bool:
        return sdmsManager.create_collection(super().get_cb_bucket_name(), super().get_cb_scope_name(), self.get_cb_collection_name(p_is_recycle))

    def drop_cb_collection(self, p_is_recycle: bool = False) -> bool:
        return sdmsManager.drop_collection(super().get_cb_bucket_name(), super().get_cb_scope_name(), self.get_cb_collection_name(p_is_recycle))

    def create_cb_primary_index(self, p_is_recycle: bool = False, p_index_name: str = None, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_index_name = "#pri_" + self.get_cb_collection_name(p_is_recycle) if p_index_name == None or len(p_index_name) == 0 else p_index_name
        return sdmsManager.create_primary_index(super().get_cb_bucket_name(), super().get_cb_scope_name(), self.get_cb_collection_name(p_is_recycle), tmp_index_name, p_num_replicas, p_ignore_if_exists, p_timeout)

    def drop_cb_primary_index(self, p_is_recycle: bool = False, p_index_name: str = None, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_index_name = "#pri_" + self.get_cb_collection_name(p_is_recycle) if p_index_name == None or len(p_index_name) == 0 else p_index_name
        return sdmsManager.drop_primary_index(super().get_cb_bucket_name(), super().get_cb_scope_name(), self.get_cb_collection_name(p_is_recycle), tmp_index_name, p_ignore_if_exists, p_timeout)

    def create_cb_key_index(self, p_is_recycle: bool = False, p_index_name: str = None, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_index_name = "pk_" + self.get_cb_collection_name() if p_index_name == None or len(p_index_name) == 0 else p_index_name
        return sdmsManager.create_index(super().get_cb_bucket_name(), super().get_cb_scope_name(), self.get_cb_collection_name(p_is_recycle), tmp_index_name, super().get_keys(), p_num_replicas, p_ignore_if_exists, p_timeout)

    def drop_cb_key_index(self, p_is_recycle: bool = False, p_index_name: str = None, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        tmp_index_name = "pk_" + self.get_cb_collection_name() if p_index_name == None or len(p_index_name) == 0 else p_index_name
        return sdmsManager.drop_index(super().get_cb_bucket_name(), super().get_cb_scope_name(), self.get_cb_collection_name(p_is_recycle), tmp_index_name, p_ignore_if_exists, p_timeout)

    def create_cb_index(self, p_index_name: str, p_fields: list, p_is_recycle: bool = False, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        return sdmsManager.create_index(super().get_cb_bucket_name(), super().get_cb_scope_name(), self.get_cb_collection_name(p_is_recycle), p_index_name, p_fields, p_num_replicas, p_ignore_if_exists, p_timeout)

    def drop_cb_index(self, p_index_name: str, p_is_recycle: bool = False, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> bool:
        return sdmsManager.drop_index(super().get_cb_bucket_name(), super().get_cb_scope_name(), self.get_cb_collection_name(p_is_recycle), p_index_name, p_ignore_if_exists, p_timeout)

    async def async_create_cb_collection(self, p_is_recycle: bool = False) -> dict:
        tmp_ret = self.create_cb_collection(p_is_recycle)
        return {"bucket_name": super().get_cb_bucket_name(), "scope_name": super().get_cb_scope_name(), "collection_name": self.get_cb_collection_name(p_is_recycle), "table_name": self.get_cb_table_name(p_is_recycle), "is_success": tmp_ret}

    async def async_drop_cb_collection(self, p_is_recycle: bool = False) -> dict:
        tmp_ret = self.drop_cb_collection(p_is_recycle)
        return {"bucket_name": super().get_cb_bucket_name(), "scope_name": super().get_cb_scope_name(), "collection_name": self.get_cb_collection_name(p_is_recycle), "table_name": self.get_cb_table_name(p_is_recycle), "is_success": tmp_ret}

    async def async_create_cb_primary_index(self, p_is_recycle: bool = False, p_index_name: str = None, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> dict:
        tmp_index_name = "#pri_" + self.get_cb_collection_name(p_is_recycle) if p_index_name == None or len(p_index_name) == 0 else p_index_name
        tmp_ret = self.create_cb_primary_index(p_is_recycle, tmp_index_name, p_num_replicas, p_ignore_if_exists, p_timeout)
        return {"bucket_name": super().get_cb_bucket_name(), "scope_name": super().get_cb_scope_name(), "collection_name": self.get_cb_collection_name(p_is_recycle), "table_name": self.get_cb_table_name(p_is_recycle), "index_name": tmp_index_name, "is_success": tmp_ret}

    async def async_drop_cb_primary_index(self, p_is_recycle: bool = False, p_index_name: str = None, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> dict:
        tmp_index_name = "#pri_" + self.get_cb_collection_name(p_is_recycle) if p_index_name == None or len(p_index_name) == 0 else p_index_name
        tmp_ret = self.drop_cb_primary_index(p_is_recycle, tmp_index_name, p_ignore_if_exists, p_timeout)
        return {"bucket_name": super().get_cb_bucket_name(), "scope_name": super().get_cb_scope_name(), "collection_name": self.get_cb_collection_name(p_is_recycle), "table_name": self.get_cb_table_name(p_is_recycle), "index_name": tmp_index_name, "is_success": tmp_ret}

    async def async_create_cb_key_index(self, p_is_recycle: bool = False, p_index_name: str = None, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> dict:
        tmp_index_name = "pk_" + self.get_cb_collection_name(p_is_recycle) if p_index_name == None or len(p_index_name) == 0 else p_index_name
        tmp_ret = self.create_cb_key_index(p_is_recycle, tmp_index_name, p_num_replicas, p_ignore_if_exists, p_timeout)
        return {"bucket_name": super().get_cb_bucket_name(), "scope_name": super().get_cb_scope_name(), "collection_name": self.get_cb_collection_name(p_is_recycle), "table_name": self.get_cb_table_name(), "index_name": tmp_index_name, "is_success": tmp_ret}

    async def async_drop_cb_key_index(self, p_is_recycle: bool = False, p_index_name: str = None, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> dict:
        tmp_index_name = "pk_" + self.get_cb_collection_name(p_is_recycle) if p_index_name == None or len(p_index_name) == 0 else p_index_name
        tmp_ret = self.drop_cb_key_index(p_is_recycle, tmp_index_name, p_ignore_if_exists, p_timeout)
        return {"bucket_name": super().get_cb_bucket_name(), "scope_name": super().get_cb_scope_name(), "collection_name": self.get_cb_collection_name(p_is_recycle), "table_name": self.get_cb_table_name(), "index_name": tmp_index_name, "is_success": tmp_ret}

    async def async_create_cb_index(self, p_index_name: str, p_fields: list, p_is_recycle: bool = False, p_num_replicas: int = 0, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> dict:
        tmp_ret = self.create_cb_index(p_index_name, p_fields, p_is_recycle, p_num_replicas, p_ignore_if_exists, p_timeout)
        return {"bucket_name": super().get_cb_bucket_name(), "scope_name": super().get_cb_scope_name(), "collection_name": self.get_cb_collection_name(p_is_recycle), "table_name": self.get_cb_table_name(), "index_name": p_index_name, "is_success": tmp_ret}

    def drop_cb_index(self, p_index_name: str, p_is_recycle: bool = False, p_ignore_if_exists: bool = False, p_timeout: timedelta = None) -> dict:
        tmp_ret = self.drop_cb_index(p_index_name, p_is_recycle, p_ignore_if_exists, p_timeout)
        return {"bucket_name": super().get_cb_bucket_name(), "scope_name": super().get_cb_scope_name(), "collection_name": self.get_cb_collection_name(p_is_recycle), "table_name": self.get_cb_table_name(), "index_name": p_index_name, "is_success": tmp_ret}

    #
    # meta data methods (couchbase 관련)
    #

    def exists(self, p_meta_id: str, p_is_recycle: bool = False) -> bool:
        return super()._exists(self.get_cb_collection(p_is_recycle), p_meta_id)

    def exists_as_id(self, p_id: str, p_is_recycle: bool = False) -> bool:
        tmp_meta_id = super()._id_to_meta_id(p_id)
        return super()._exists(self.get_cb_collection(p_is_recycle), tmp_meta_id)

    def get(self, p_meta_id: str, p_is_recycle: bool = False, p_erase_history_key: bool = True) -> dict:
        return super()._get(self.get_cb_collection(p_is_recycle), p_meta_id, p_erase_history_key)

    def get_as_id(self, p_id: str, p_is_recycle: bool = False, p_erase_history_key: bool = True) -> dict:
        tmp_meta_id = super()._id_to_meta_id(p_id)
        return super()._get(self.get_cb_collection(p_is_recycle), tmp_meta_id, p_erase_history_key)

    def remove(self, p_meta_id: str, p_is_recycle: bool = False) -> bool:
        return super()._remove(self.get_cb_collection(p_is_recycle), p_meta_id)

    def remove_as_id(self, p_id: str, p_is_recycle: bool = False) -> bool:
        tmp_meta_id = super()._id_to_meta_id(p_id)
        return super()._remove(self.get_cb_collection(p_is_recycle), tmp_meta_id)

    def insert(self, p_data_dict: dict, p_actor_id: str, p_is_recycle: bool = False) -> bool:
        tmp_meta_id = super()._inner_check_key(p_data_dict, True)
        return super()._insert(self.get_cb_collection(p_is_recycle), tmp_meta_id, p_data_dict, p_actor_id)

    def upsert(self, p_data_dict: dict, p_actor_id: str, p_is_recycle: bool = False) -> bool:
        tmp_meta_id = super()._inner_check_key(p_data_dict, True)
        return super()._upsert(self.get_cb_collection(p_is_recycle), tmp_meta_id, p_data_dict, p_actor_id)

    def mutate_in(self, p_meta_id: str, p_sub_document_cmd_list: list, p_actor_id: str, p_is_recycle: bool = False) -> bool:
        return super()._mutate_in(self.get_cb_collection(p_is_recycle), p_meta_id, p_sub_document_cmd_list, p_actor_id)

    def mutate_in_as_id(self, p_id: str, p_sub_document_cmd_list: list, p_actor_id: str, p_is_recycle: bool = False) -> bool:
        temp_meta_id = super()._id_to_meta_id(p_id)
        return super()._mutate_in(self.get_cb_collection(p_is_recycle), temp_meta_id, p_sub_document_cmd_list, p_actor_id)

    async def async_get(self, p_meta_id: str, p_is_recycle: bool = False, p_erase_history_key: bool = True) -> dict:
        tmp_ret_dict = super()._get(self.get_cb_collection(p_is_recycle), p_meta_id, p_erase_history_key)
        return {"meta_id": p_meta_id, "meta_data": tmp_ret_dict}

    async def async_get_as_id(self, p_id: str, p_is_recycle: bool = False, p_erase_history_key: bool = True) -> dict:
        tmp_meta_id = super()._id_to_meta_id(p_id)
        tmp_ret_dict = super()._get(self.get_cb_collection(p_is_recycle), tmp_meta_id, p_erase_history_key)
        return {"id": p_id, "meta_id": tmp_meta_id, "meta_data": tmp_ret_dict}

    async def async_remove(self, p_meta_id: str, p_is_recycle: bool = False) -> dict:
        tmp_ret = super()._remove(self.get_cb_collection(p_is_recycle), p_meta_id)
        return {"meta_id": p_meta_id, "is_success": tmp_ret}

    async def async_remove_as_id(self, p_id: str, p_is_recycle: bool = False) -> dict:
        tmp_meta_id = super()._id_to_meta_id(p_id)
        tmp_ret = super()._remove(self.get_cb_collection(p_is_recycle), tmp_meta_id)
        return {"id": p_id, "meta_id": tmp_meta_id, "is_success": tmp_ret}

    async def async_insert(self, p_data_dict: dict, p_actor_id: str, p_is_recycle: bool = False) -> dict:
        tmp_meta_id = super()._inner_check_key(p_data_dict, True)
        tmp_ret = super()._insert(self.get_cb_collection(p_is_recycle), tmp_meta_id, p_data_dict, p_actor_id)
        return {"meta_id": tmp_meta_id, "is_success": tmp_ret}

    async def async_upsert(self, p_data_dict: dict, p_actor_id: str, p_is_recycle: bool = False) -> dict:
        tmp_meta_id = super()._inner_check_key(p_data_dict, True)
        tmp_ret = super()._upsert(self.get_cb_collection(p_is_recycle), tmp_meta_id, p_data_dict, p_actor_id)
        return {"meta_id": tmp_meta_id, "is_success": tmp_ret}

    async def async_mutate_in(self, p_meta_id: str, p_sub_document_cmd_list: list, p_actor_id: str, p_is_recycle: bool = False) -> dict:
        tmp_ret = super()._mutate_in(self.get_cb_collection(p_is_recycle), p_meta_id, p_sub_document_cmd_list, p_actor_id)
        return {"meta_id": p_meta_id, "is_success": tmp_ret}

    async def async_mutate_in_as_id(self, p_id: str, p_sub_document_cmd_list: list, p_actor_id: str, p_is_recycle: bool = False) -> dict:
        tmp_meta_id = super()._id_to_meta_id(p_id)
        tmp_ret = super()._mutate_in(self.get_cb_collection(p_is_recycle), tmp_meta_id, p_sub_document_cmd_list, p_actor_id)
        return {"id": p_id, "meta_id": tmp_meta_id, "is_success": tmp_ret}

    #
    # n1ql (couchbase 관련)
    #

    def select_count(self, query: str, p_is_recycle: bool = False, query_option: QueryOptions = None, **kwargs) -> int:
        kwargs["P_BUCKET"] = self.get_cb_bucket_name()
        kwargs["P_TABLE"] = self.get_cb_table_name(p_is_recycle)

        kwargs["p_bucket"] = self.get_cb_bucket_name()
        kwargs["p_table"] = self.get_cb_table_name(p_is_recycle)

        tmp_site_id = self.get_site_id()
        if tmp_site_id != None and len(tmp_site_id) > 0:
            kwargs["P_SITE_ID"] = tmp_site_id
            kwargs["p_site_id"] = tmp_site_id

        return sdmsN1ql.select_count(query, query_option, **kwargs)

    def select_list(self, query: str, p_is_recycle: bool = False, query_option: QueryOptions = None, **kwargs) -> pd.DataFrame:
        kwargs["P_BUCKET"] = self.get_cb_bucket_name()
        kwargs["P_TABLE"] = self.get_cb_table_name(p_is_recycle)

        kwargs["p_bucket"] = self.get_cb_bucket_name()
        kwargs["p_table"] = self.get_cb_table_name(p_is_recycle)

        tmp_site_id = self.get_site_id()
        if tmp_site_id != None and len(tmp_site_id) > 0:
            kwargs["P_SITE_ID"] = tmp_site_id
            kwargs["p_site_id"] = tmp_site_id

        return sdmsN1ql.select_list(query, query_option, **kwargs)

    def select_result(self, query: str, p_is_recycle: bool = False, query_option: QueryOptions = None, **kwargs) -> QueryResult:
        kwargs["P_BUCKET"] = self.get_cb_bucket_name()
        kwargs["P_TABLE"] = self.get_cb_table_name(p_is_recycle)

        kwargs["p_bucket"] = self.get_cb_bucket_name()
        kwargs["p_table"] = self.get_cb_table_name(p_is_recycle)

        tmp_site_id = self.get_site_id()
        if tmp_site_id != None and len(tmp_site_id) > 0:
            kwargs["P_SITE_ID"] = tmp_site_id
            kwargs["p_site_id"] = tmp_site_id

        return sdmsN1ql.select_result(query, query_option, **kwargs)

    def select_page_list(self, query: str, page_num: int, page_length: int, p_is_recycle: bool = False, query_option: QueryOptions = None, **kwargs) -> pd.DataFrame:
        kwargs["P_BUCKET"] = self.get_cb_bucket_name()
        kwargs["P_TABLE"] = self.get_cb_table_name(p_is_recycle)

        kwargs["p_bucket"] = self.get_cb_bucket_name()
        kwargs["p_table"] = self.get_cb_table_name(p_is_recycle)

        tmp_site_id = self.get_site_id()
        if tmp_site_id != None and len(tmp_site_id) > 0:
            kwargs["P_SITE_ID"] = tmp_site_id
            kwargs["p_site_id"] = tmp_site_id

        return sdmsN1ql.select_page_list(query, page_num, page_length, query_option, **kwargs)

    async def asyn_select_count(self, key: str, query: str, p_is_recycle: bool = False, query_option: QueryOptions = None, **kwargs) -> dict:
        kwargs["P_BUCKET"] = self.get_cb_bucket_name()
        kwargs["P_TABLE"] = self.get_cb_table_name(p_is_recycle)

        kwargs["p_bucket"] = self.get_cb_bucket_name()
        kwargs["p_table"] = self.get_cb_table_name(p_is_recycle)

        tmp_site_id = self.get_site_id()
        if tmp_site_id != None and len(tmp_site_id) > 0:
            kwargs["P_SITE_ID"] = tmp_site_id
            kwargs["p_site_id"] = tmp_site_id

        tmp_ret_cnt = sdmsN1ql.select_count(query, query_option, **kwargs)
        return {"key": key, "count": tmp_ret_cnt}

    async def async_select_list(self, key: str, query: str, p_is_recycle: bool = False, query_option: QueryOptions = None, **kwargs) -> dict:
        kwargs["P_BUCKET"] = self.get_cb_bucket_name()
        kwargs["P_TABLE"] = self.get_cb_table_name(p_is_recycle)

        kwargs["p_bucket"] = self.get_cb_bucket_name()
        kwargs["p_table"] = self.get_cb_table_name(p_is_recycle)

        tmp_site_id = self.get_site_id()
        if tmp_site_id != None and len(tmp_site_id) > 0:
            kwargs["P_SITE_ID"] = tmp_site_id
            kwargs["p_site_id"] = tmp_site_id

        tmp_ret_list = sdmsN1ql.select_list(query, query_option, **kwargs)
        return {"key": key, "dataframe": tmp_ret_list}

    async def async_select_result(self, key: str, query: str, p_is_recycle: bool = False, query_option: QueryOptions = None, **kwargs) -> dict:
        kwargs["P_BUCKET"] = self.get_cb_bucket_name()
        kwargs["P_TABLE"] = self.get_cb_table_name(p_is_recycle)

        kwargs["p_bucket"] = self.get_cb_bucket_name()
        kwargs["p_table"] = self.get_cb_table_name(p_is_recycle)

        tmp_site_id = self.get_site_id()
        if tmp_site_id != None and len(tmp_site_id) > 0:
            kwargs["P_SITE_ID"] = tmp_site_id
            kwargs["p_site_id"] = tmp_site_id

        tmp_ret_result = sdmsN1ql.select_result(query, query_option, **kwargs)
        return {"key": key, "result": tmp_ret_result}

    async def async_select_page_list(self, key: str, query: str, page_num: int, page_length: int, p_is_recycle: bool = False, query_option: QueryOptions = None, **kwargs) -> dict:
        kwargs["P_BUCKET"] = self.get_cb_bucket_name()
        kwargs["P_TABLE"] = self.get_cb_table_name(p_is_recycle)

        kwargs["p_bucket"] = self.get_cb_bucket_name()
        kwargs["p_table"] = self.get_cb_table_name(p_is_recycle)

        tmp_site_id = self.get_site_id()
        if tmp_site_id != None and len(tmp_site_id) > 0:
            kwargs["P_SITE_ID"] = tmp_site_id
            kwargs["p_site_id"] = tmp_site_id

        tmp_ret_list = sdmsN1ql.select_page_list(query, page_num, page_length, query_option, **kwargs)
        return {"key": key, "page_num": page_num, "page_length": page_length, "dataframe": tmp_ret_list}
