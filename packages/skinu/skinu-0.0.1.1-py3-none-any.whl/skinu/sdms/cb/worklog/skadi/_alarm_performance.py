from couchbase.collection import Collection

from skinu.core import str_utils
import skinu.sdms as sdms
from skinu.sdms.cb._base_single_document import sdmsBaseSingleDocument


#
# class sdms_meta_info
#
class sdms_meta_info:
    _meta_bucket_name = "WORKLOG"
    _meta_scope_name = "skadi"
    _meta_collection_name = "alarm_performance"

    _meta_filed_dict: dict = {
        "site_id": "",
        "alarm_id": "",
        "performance_logic_id": "",
        "prop_performance_chart_type": "",
        "description": "",
        "recommended": "",
        "diagnosis": "",
        "actual": {
            "head": None,
            "shaft_power": None,
            "pump_efficiency": None,
            "flow": None,
        },
        "design": {
            "head": None,
            "shaft_power": None,
            "pump_efficiency": None,
            "flow": None,
        },
        "model": {
            "head_type": "",
            "x_min": 0,
            "x_max": 0,
            "flow_min": 0,
            "head_x6": 0.0,
            "head_x5": 0.0,
            "head_x4": 0.0,
            "head_x3": 0.0,
            "head_x2": 0.0,
            "head_x1": 0.0,
            "head_x0": 0.0,
            "power_x6": 0.0,
            "power_x5": 0.0,
            "power_x4": 0.0,
            "power_x3": 0.0,
            "power_x2": 0.0,
            "power_x1": 0.0,
            "power_x0": 0.0,
            "efficiency_x6": 0.0,
            "efficiency_x5": 0.0,
            "efficiency_x4": 0.0,
            "efficiency_x3": 0.0,
            "efficiency_x2": 0.0,
            "efficiency_x1": 0.0,
            "efficiency_x0": 0.0,
            "head_unit": "",
            "power_unit": "",
            "efficiency_unit": "",
            "flow_unit": "",
        },
    }

    _meta_version: int = 1

    _meta_document_info_dict: dict = {
        "keyset": [
            {"id": "alarm_id", "type": "str"},
        ],
    }

    def _request_upgrade_collection_meta_data(p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        pass


#
# class sdmsAlarmPerformance
#
class sdmsAlarmPerformance(sdmsBaseSingleDocument):
    def __init__(self, p_site_id: str = "", p_user_document_name: str = ""):
        tmp_sdms_config = sdms.sdms_get_config()
        tmp_bucket_name = sdms_meta_info._meta_bucket_name if tmp_sdms_config == None else tmp_sdms_config.bucket_name_worklog
        tmp_scope_name = sdms_meta_info._meta_scope_name
        tmp_collection_name = sdms_meta_info._meta_collection_name
        tmp_document_name = tmp_collection_name if str_utils.is_empty_str(p_user_document_name) == True else p_user_document_name
        super().__init__(tmp_bucket_name, tmp_scope_name, tmp_collection_name, tmp_document_name, p_site_id, sdms_meta_info._meta_filed_dict, sdms_meta_info._meta_version, sdms_meta_info._meta_document_info_dict, True)

    #
    # abstract method 관련
    #

    def _request_upgrade_meta_data(self, p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        sdms_meta_info._request_upgrade_collection_meta_data(p_cb_collection, p_data_dict, p_meta_verion, p_document_version)
