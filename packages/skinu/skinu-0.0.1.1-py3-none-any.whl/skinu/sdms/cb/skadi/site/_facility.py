from couchbase.collection import Collection

from skinu.core import str_utils
from skinu.core import dict_utils
import skinu.sdms as sdms
from skinu.sdms.cb._base_single_document import sdmsBaseSingleDocument


#
# class sdms_meta_info
#
class sdms_meta_info:
    _meta_bucket_name = "SKADI"
    _meta_scope_name = "site"
    _meta_collection_name = "facility"

    _meta_filed_dict: dict = {
        "site_id": "",
        "facility_id": "",
        "prop_facility_type": "",
        "name": "",
        "description": "",
        "parent_id": "",
    }

    _meta_version: int = 1

    _meta_document_info_dict: dict = {
        "keyset": [
            {"id": "facility_id", "type": "str"},
        ],
    }

    def _request_upgrade_collection_meta_data(p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        pass


#
# class sdmsFacility
#
class sdmsFacility(sdmsBaseSingleDocument):
    def __init__(self, p_site_id: str = "", p_user_document_name: str = ""):
        tmp_sdms_config = sdms.sdms_get_config()
        tmp_bucket_name = sdms_meta_info._meta_bucket_name if tmp_sdms_config == None else tmp_sdms_config.bucket_name_skadi
        tmp_scope_name = sdms_meta_info._meta_scope_name
        tmp_collection_name = sdms_meta_info._meta_collection_name
        tmp_document_name = tmp_collection_name if str_utils.is_empty_str(p_user_document_name) == True else p_user_document_name
        super().__init__(tmp_bucket_name, tmp_scope_name, tmp_collection_name, tmp_document_name, p_site_id, sdms_meta_info._meta_filed_dict, sdms_meta_info._meta_version, sdms_meta_info._meta_document_info_dict, True)

    #
    # abstract method 관련
    #

    def _request_upgrade_meta_data(self, p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        sdms_meta_info._request_upgrade_collection_meta_data(p_cb_collection, p_data_dict, p_meta_verion, p_document_version)

    #
    # facility 상위 정보 가져 오기 (본인 포함)
    #
    def get_tree_up_info(self, p_facility_id: str) -> dict:
        tmp_ret_dict = dict()

        tmp_search_facility_id = p_facility_id
        while str_utils.is_not_empty_str(tmp_search_facility_id) == True:
            tmp_dict = self.get_as_id(tmp_search_facility_id)
            if tmp_dict != None:
                tmp_prop_factility_type = dict_utils.get_str(tmp_dict, "prop_facility_type", "")
                tmp_prop_factility_id = dict_utils.get_str(tmp_dict, "facility_id", "")
                tmp_prop_factility_name = dict_utils.get_str(tmp_dict, "name", "")
                tmp_parent_id = dict_utils.get_str(tmp_dict, "parent_id", "")

                if str_utils.is_not_empty_str(tmp_prop_factility_type) == True:
                    tmp_ret_dict[tmp_prop_factility_type] = {
                        "id": tmp_prop_factility_id,
                        "name": tmp_prop_factility_name,
                    }

                tmp_search_facility_id = tmp_parent_id
            else:
                tmp_search_facility_id = ""

        return tmp_ret_dict
