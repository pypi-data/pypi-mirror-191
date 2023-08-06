import copy
from datetime import datetime
from abc import *

from couchbase.bucket import Bucket
from couchbase.scope import Scope
from couchbase.collection import Collection
import couchbase.subdocument as SD
from couchbase.exceptions import DocumentExistsException, DocumentNotFoundException

from skinu._internal._logs import _skinuLog
from skinu.core import dict_utils
from skinu.core import str_utils
import skinu.sdms as sdms


#
# class sdmsBaseDocument
#
class sdmsBaseDocument(metaclass=ABCMeta):
    def __init__(self,
                 p_cb_bucket_name: str,
                 p_cb_scope_name: str,
                 p_cb_collection_name: str,
                 p_cb_document_name: str,
                 p_site_id: str,
                 p_meta_field_dict: dict,
                 p_meta_version: int,
                 p_meta_document_info_dict: dict,
                 p_is_exist_update_time_field: bool):
        self.__cb_bucket_name = p_cb_bucket_name
        self.__cb_scope_name = p_cb_scope_name
        self.__cb_collection_name = p_cb_collection_name
        self.__cb_document_name = p_cb_document_name
        self.__site_id = p_site_id
        self.__meta_field_dict = copy.deepcopy(p_meta_field_dict)
        self.__meta_version = p_meta_version
        self.__meta_document_info_dict = copy.deepcopy(p_meta_document_info_dict)
        self.__is_exist_update_time_field = p_is_exist_update_time_field

        self.__is_exist_site_id = False if (p_site_id is None) or (len(p_site_id) == 0) else True

    #
    # abstract methods 관련
    #

    @abstractmethod
    def _request_upgrade_meta(self, p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        nie = NotImplementedError("not implemented _request_upgrade_meta method")
        _skinuLog.getLogger().critical(nie)
        raise nie

    #
    # private methods
    #
    def _inner_check_key(self, p_data_dict: dict, p_ret_meta_id=False) -> str:
        tmp_ret_meta_id = ""

        # site_id 검사
        if self.__is_exist_site_id == True and len(self.__site_id) == 0:
            e = Exception("No exist key fields [site_id]")
            _skinuLog.getLogger().critical(e)
            raise e

        # document 명칭 검사
        if self.__cb_document_name == None or len(self.__cb_document_name) == 0:
            e = Exception("No exist unknown document name")
            _skinuLog.getLogger().critical(e)
            raise e

        # keyset 검사
        tmp_keyset = dict_utils.get_object(self.__meta_document_info_dict, "keyset", [])
        tmp_keyset_id = ""
        for tmp_key in tmp_keyset:
            tmp_key_id = tmp_key["id"]
            tmp_key_type = tmp_key["type"]

            if tmp_key_type == "S" or tmp_key_type == "str":
                tmp_key_str_data = dict_utils.get_str(p_data_dict, tmp_key_id, None)
                if tmp_key_str_data == None or len(tmp_key_str_data) == 0:
                    e = Exception("No exist key field [{0}]".format(tmp_key))
                    _skinuLog.getLogger().critical(e)
                    raise e

                tmp_keyset_id = tmp_keyset_id + "_" + tmp_key_str_data

            elif tmp_key_type == "I" or tmp_key_type == "int":
                tmp_key_int_data = dict_utils.get_int(p_data_dict, tmp_key_id, None)
                if tmp_key_int_data == None:
                    e = Exception("No exist key field [{0}]".format(tmp_key))
                    _skinuLog.getLogger().critical(e)
                    raise e

                tmp_keyset_id = tmp_keyset_id + "_" + str(tmp_key_int_data)

            elif tmp_key_type == "F" or tmp_key_type == "float":
                tmp_key_float_data = dict_utils.get_float(p_data_dict, tmp_key_id, None)
                if tmp_key_float_data == None:
                    e = Exception("No exist key field [{0}]".format(tmp_key))
                    _skinuLog.getLogger().critical(e)
                    raise e

                tmp_keyset_id = tmp_keyset_id + "_" + str(tmp_key_float_data)

            else:
                e = Exception("No exist key unknown type field [{0}]".format(tmp_key))
                _skinuLog.getLogger().critical(e)
                raise e

        if p_ret_meta_id == True:
            tmp_ret_meta_id = ("" if self.__is_exist_site_id == False else (self.__site_id + "_")) + self.__cb_document_name + tmp_keyset_id

        return tmp_ret_meta_id

    def _id_to_meta_id(self, p_id: str) -> str:
        tmp_meta_id = ""

        # site_id 검사
        if self.__is_exist_site_id == True and len(self.__site_id) == 0:
            e = Exception("No exist key fields [site_id]")
            _skinuLog.getLogger().critical(e)
            raise e

        # document 명칭 추가
        if self.__cb_document_name == None or len(self.__cb_document_name) == 0:
            e = Exception("No exist unknown document name")
            _skinuLog.getLogger().critical(e)
            raise e

        tmp_meta_id = ("" if self.__is_exist_site_id == False else (self.__site_id + "_")) + self.__cb_document_name + ("" if len(p_id) == 0 else "_") + p_id

        return tmp_meta_id

    #
    # get (couchbase 관련)
    #

    def get_cb_bucket(self) -> Bucket:
        return sdms.sdms_get_cluster().bucket(self.__cb_bucket_name)

    def get_cb_scope(self) -> Scope:
        return sdms.sdms_get_cluster().bucket(self.__cb_bucket_name).scope(self.__cb_scope_name)

    def get_cb_bucket_name(self) -> str:
        return self.__cb_bucket_name

    def get_cb_scope_name(self) -> str:
        return self.__cb_scope_name

    def _get_cb_collection_name(self) -> str:
        return self.__cb_collection_name

    def get_cb_document_name(self) -> str:
        return self.__cb_document_name

    #
    # get (meta 정보 관련)
    #

    def is_exist_site_id(self) -> bool:
        return self.__is_exist_site_id

    def get_site_id(self) -> str:
        return self.__site_id

    def get_meta_version(self) -> int:
        return self.__meta_version

    def get_meta_id(self, p_data_dict: dict = None) -> str:
        return self._inner_check_key(p_data_dict if p_data_dict != None else {}, True)

    def is_exist_updated_time_field(self) -> bool:
        return self.__is_exist_update_time_field

    def get_init_meta_data(self, p_data_dict: dict = None, p_check_key: bool = False) -> dict:
        if p_check_key == True:
            self._inner_check_key(p_data_dict, False)

        # 초기 데이터 넣기
        tmp_ret_meta_dict = copy.deepcopy(self.__meta_field_dict)

        if p_data_dict != None:
            tmp_ret_meta_dict.update(p_data_dict)

        # site_id 정보 넣기
        if self.__is_exist_site_id != None:
            tmp_ret_meta_dict["site_id"] = self.__site_id

        return tmp_ret_meta_dict

    def get_keys(self) -> list:
        tmp_keys = []

        if self.__is_exist_site_id == True:
            tmp_keys.append("site_id")

        tmp_keyset = dict_utils.get_object(self.__meta_document_info_dict, "keyset", [])
        for tmp_key in tmp_keyset:
            tmp_keys.append(tmp_key["id"])

        return tmp_keys

    #
    # meta data methods (couchbase 관련)
    #

    def _exists(self, p_cb_collection: Collection, p_meta_id: str) -> bool:
        res = p_cb_collection.exists(p_meta_id)
        return res.exists

    def _get(self, p_cb_collection: Collection, p_meta_id: str, p_erase_history_key: bool = True) -> dict:
        # 데이터 가져 오기
        tmp_ret_dict: dict = None

        try:
            tmp_ret_res = p_cb_collection.get(p_meta_id)
            tmp_ret_dict = tmp_ret_res.content_as[dict]

            # 버젼이 동일하지 않는 경우 업데이트 처리를 해 준다
            temp_version = dict_utils.get_int(tmp_ret_dict, "version", None)
            if temp_version == None or temp_version != self.__meta_version:
                self._request_upgrade_meta(p_cb_collection, tmp_ret_dict, self.__meta_version, temp_version)

            # 불필요한 데이터 삭제
            if p_erase_history_key == True:
                tmp_ret_dict.pop("created_at", None)
                tmp_ret_dict.pop("created_id", None)
                tmp_ret_dict.pop("updated_at", None)
                tmp_ret_dict.pop("updated_id", None)
                tmp_ret_dict.pop("version", None)

        except DocumentNotFoundException as dnfe:
            _skinuLog.getLogger().debug(dnfe)
            tmp_ret_dict = None

        return tmp_ret_dict

    def _remove(self, p_cb_collection: Collection, p_meta_id: str) -> bool:
        # 데이터 삭제 하기
        tmp_ret = False

        try:
            p_cb_collection.remove(p_meta_id)
            tmp_ret = True

        except DocumentNotFoundException as dnfe:
            print(dnfe)
            _skinuLog.getLogger().debug(dnfe)
            tmp_ret = False

        return tmp_ret

    def _insert(self, p_cb_collection: Collection, p_meta_id: str, p_data_dict: dict, p_actor_id: str) -> bool:
        # 기본 데이터 가져 오기
        tmp_meta_dict = copy.deepcopy(self.__meta_field_dict)
        tmp_meta_dict.update(p_data_dict)

        # 부가 정보 넣기

        # site_id 정보 넣기
        if self.__is_exist_site_id == True:
            tmp_meta_dict["site_id"] = self.__site_id

        # 현재 일자
        tmp_now_datetime = datetime.now()
        tmp_now_datetime_s = tmp_now_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # insert 일자
        tmp_meta_dict["created_at"] = tmp_now_datetime_s
        tmp_meta_dict["created_id"] = p_actor_id

        # update 일자
        if self.__is_exist_update_time_field == True:
            tmp_meta_dict["updated_at"] = tmp_now_datetime_s
            tmp_meta_dict["updated_id"] = p_actor_id

        # 버젼 정보
        tmp_meta_dict["version"] = self.__meta_version

        tmp_ret = False
        try:
            p_cb_collection.insert(p_meta_id, tmp_meta_dict)
            tmp_ret = True
        except DocumentExistsException as dee:
            _skinuLog.getLogger().debug(dee)
            tmp_ret = False
        except Exception as e:
            _skinuLog.getLogger().debug(e)
            tmp_ret = False

        return tmp_ret

    def _upsert(self, p_cb_collection: Collection, p_meta_id: str, p_data_dict: dict, p_actor_id: str) -> bool:
        # 기본 데이터 가져 오기
        tmp_meta_dict = copy.deepcopy(self.__meta_field_dict)
        tmp_meta_dict.update(p_data_dict)

        # 부가 정보 넣기

        # site_id 정보 넣기
        if self.__is_exist_site_id == True:
            tmp_meta_dict["site_id"] = self.__site_id

        # 현재 일자
        tmp_now_datetime = datetime.now()
        tmp_now_datetime_s = tmp_now_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # insert 일자
        tmp_meta_dict["created_at"] = tmp_now_datetime_s
        tmp_meta_dict["created_id"] = p_actor_id

        # 기존 생성정보 가져 오기
        try:
            tmp_ret_res = p_cb_collection.lookup_in(p_meta_id, (SD.get('created_at'), SD.get('created_id'),))
            tmp_created_at = tmp_ret_res.content_as[str](0)
            tmp_created_id = tmp_ret_res.content_as[str](1)

            tmp_meta_dict["created_at"] = tmp_now_datetime_s if str_utils.is_empty_str(tmp_created_at) else tmp_created_at
            tmp_meta_dict["created_id"] = p_actor_id if str_utils.is_empty_str(tmp_created_id) else tmp_created_id
        except DocumentNotFoundException as dnfe:
            pass

        # update 일자
        if self.__is_exist_update_time_field == True:
            tmp_meta_dict["updated_at"] = tmp_now_datetime_s
            tmp_meta_dict["updated_id"] = p_actor_id

        # 버젼 정보
        tmp_meta_dict["version"] = self.__meta_version

        # 데이터 넣기
        temp_ret = True
        p_cb_collection.upsert(p_meta_id, tmp_meta_dict)

        return temp_ret

    def _mutate_in(self, p_cb_collection: Collection, p_meta_id: str, p_sub_document_cmd_list: list, p_actor_id: str) -> bool:
        tmp_updated_list = []

        # update 일자
        if self.__is_exist_update_time_field == True:
            # 현재 일자
            tmp_now_datetime = datetime.now()
            tmp_now_datetime_s = tmp_now_datetime.strftime("%Y-%m-%d %H:%M:%S")

            tmp_updated_list.append(SD.upsert("updated_at", tmp_now_datetime_s, create_parents=True))
            tmp_updated_list.append(SD.upsert("updated_id", p_actor_id, create_parents=True))

        tmp_ret = False
        try:
            if self.__is_exist_update_time_field == True:
                p_cb_collection.mutate_in(p_meta_id, tmp_updated_list)

            p_cb_collection.mutate_in(p_meta_id, p_sub_document_cmd_list)
            tmp_ret = True
        except DocumentNotFoundException as dnfe:
            _skinuLog.getLogger().debug(dnfe)
            tmp_ret = False

        return tmp_ret
