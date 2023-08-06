from couchbase.collection import Collection

from skinu.core import str_utils
import skinu.sdms as sdms
from skinu.sdms.cb._base_single_document import sdmsBaseSingleDocument


#
# class sdms_meta_info
#
class sdms_meta_info:
    _meta_bucket_name = "SKADI"
    _meta_scope_name = "site"
    _meta_collection_name = "equip_tag"

    _meta_filed_dict: dict = {
        "site_id": "",
        "equip_id": "",
        "tag_id": "",
        "standard_tag_id": "",
        "tag_unit": "",
        "de_nde": "",
        "train": None,
        "process": None,
        "stage": None,
        "cylinder": None,
        "position": "",
        "is_gb": False,
        "run_identify_low_val": None,
        "limit_val": {
            "trip_low": None,
            "alarm_low": None,
            "soft_low": None,
            "soft_high": None,
            "alarm_high": None,
            "trip_high": None,
        },
        "logic_val": {
            "offset_high": None,
            "offset_low": None,
        }
    }

    _meta_version: int = 1

    _meta_document_info_dict: dict = {
        "keyset": [
            {"id": "equip_id", "type": "str"},
            {"id": "tag_id", "type": "str"},
        ],
    }

    def _request_upgrade_collection_meta_data(p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        pass


#
# class sdmsEquipTag
#
class sdmsEquipTag(sdmsBaseSingleDocument):
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
