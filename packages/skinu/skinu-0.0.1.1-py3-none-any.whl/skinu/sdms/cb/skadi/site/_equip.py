from couchbase.collection import Collection

from skinu.core import str_utils, dict_utils
import skinu.sdms as sdms
from skinu.sdms.cb._base_single_document import sdmsBaseSingleDocument


#
# class sdms_meta_info
#
class sdms_meta_info:
    _meta_bucket_name = "SKADI"
    _meta_scope_name = "site"
    _meta_collection_name = "equip"

    _meta_filed_dict: dict = {
        "site_id": "",
        "equip_id": "",
        "rep_prop_item_type": "",
        "item_types": [],
        "is_run": True,
        "is_est": False,
        "is_performance": False,
        "last_est_issue_dtmi": 190001010000,
        "last_performance_issue_dtmi": 190001010000,
        "tag_ids": [],
        "lab_tag_ids": [],
        "current_reference_model_id": "",
        "reference_model_ids": [],
        "performance_model_ids": [],
        "ocean_id": "",
        "tdms_url": "",
        "ocean_url": "",
        "cost_of_production_lost": 0,
        "cost_of_maintenance": 0,
        "is_used": True,
    }

    _meta_version: int = 1

    _meta_document_info_dict: dict = {
        "keyset": [
            {"id": "equip_id", "type": "str"},
        ],
    }

    def _request_upgrade_collection_meta_data(p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        pass


#
# class sdmsEquip
#
class sdmsEquip(sdmsBaseSingleDocument):
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

    def get_last_est_issue_dtmi(self, p_equip_id: str) -> int:
        tmp_doc_dict = self.get_as_id(p_equip_id)

        tmp_val = dict_utils.get_int(tmp_doc_dict, "last_est_issue_dtmi")
        # 초기 값으로 들어가 있을 경우 None으로 리턴
        if tmp_val == 190001010000:
            tmp_last_est_issue_dtmi = None
        else:
            tmp_last_est_issue_dtmi = tmp_val

        return tmp_last_est_issue_dtmi
