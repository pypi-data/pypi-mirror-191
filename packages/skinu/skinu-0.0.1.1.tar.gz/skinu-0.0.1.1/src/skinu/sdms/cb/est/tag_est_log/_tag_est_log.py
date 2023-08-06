import datetime as datetime
from datetime import timedelta

from couchbase.collection import Collection

from skinu.core import str_utils
from skinu.core import dict_utils
from skinu.core import datetime_utils
import skinu.sdms as sdms
from skinu.sdms.cb._base_single_document import sdmsBaseSingleDocument


#
# class sdms_meta_info
#
class sdms_meta_info:
    _meta_bucket_name = "EST"
    _meta_scope_name = "tag_est_log"
    _meta_collection_name = "tag_est_log"

    _meta_filed_dict: dict = {
        "site_id": "",
        "equip_id": "",
        "tag_id": "",
        "issue_dt": 19000101,
        "items": {}
    }

    _meta_version: int = 1

    _meta_document_info_dict: dict = {
        "keyset": [
            {"id": "equip_id", "type": "str"},
            {"id": "tag_id", "type": "str"},
            {"id": "issue_dt", "type": "int"},
        ],
    }

    def _request_upgrade_collection_meta_data(p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        pass


#
# class sdmsTagEstLog
#
class sdmsTagEstLog(sdmsBaseSingleDocument):
    def __init__(self, p_site_id: str = "", p_user_document_name: str = ""):
        tmp_sdms_config = sdms.sdms_get_config()
        tmp_bucket_name = sdms_meta_info._meta_bucket_name if tmp_sdms_config == None else tmp_sdms_config.bucket_name_est
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
    # 데이터 가져 오기
    #

    def get_range_chart_items(self, p_equip_id, p_tag_id: str, p_from_dtmi: int, p_to_dtmi: int, p_is_act: bool, p_is_est: bool, p_is_dev: bool, p_ts_format: str = None, p_fixed_size: int = None) -> dict:
        # 날짜 변경
        p_from_dtmi = int(p_from_dtmi / 10) * 10

        tmp_from_datetime = datetime.datetime.strptime(str(p_from_dtmi), "%Y%m%d%H%M")
        tmp_to_datetime = datetime.datetime.strptime(str(p_to_dtmi), "%Y%m%d%H%M")

        tmp_from_dtmi = datetime_utils.to_int_dtmi(tmp_from_datetime)
        tmp_to_dtmi = datetime_utils.to_int_dtmi(tmp_to_datetime)

        tmp_from_dt = datetime_utils.to_int_dt(tmp_from_datetime)
        tmp_to_dt = datetime_utils.to_int_dt(tmp_to_datetime)

        tmp_cur_dt = tmp_from_dt
        tmp_ts = []
        tmp_act_item = []
        tmp_est_item = []
        tmp_dev_item = []
        tmp_is_all_none = True
        while tmp_cur_dt <= tmp_to_dt:
            tmp_doc_id = "{}_{}_{}".format(p_equip_id, p_tag_id, tmp_cur_dt)
            tmp_doc_dict = self.get_as_id(tmp_doc_id)
            tmp_item_dict = dict_utils.get_object(tmp_doc_dict, "items", None)

            tmp_item_from_dtmi = tmp_from_dtmi if tmp_cur_dt == tmp_from_dt else int(str(tmp_cur_dt) + "0000")
            tmp_item_to_dtmi = tmp_to_dtmi if tmp_cur_dt == tmp_to_dt else int(str(tmp_cur_dt) + "2359")
            tmp_item_cur_dtmi = tmp_item_from_dtmi

            while tmp_item_cur_dtmi <= tmp_item_to_dtmi:
                tmp_item_dtmi_dict = dict_utils.get_object(tmp_item_dict, str(tmp_item_cur_dtmi), None)

                if p_is_act == True:
                    tmp_act_val = dict_utils.get_float(tmp_item_dtmi_dict, "act", None)
                    if tmp_act_val != None:
                        tmp_is_all_none = False
                    tmp_act_item.append(None if tmp_act_val == None else (round(tmp_act_val, p_fixed_size) if p_fixed_size != None else tmp_act_val))

                if p_is_est == True:
                    tmp_est_val = dict_utils.get_float(tmp_item_dtmi_dict, "est", None)
                    if tmp_est_val != None:
                        tmp_is_all_none = False
                    tmp_est_item.append(None if tmp_est_val == None else (round(tmp_est_val, p_fixed_size) if p_fixed_size != None else tmp_est_val))

                if p_is_dev == True:
                    tmp_dev_val = dict_utils.get_float(tmp_item_dtmi_dict, "dev", None)
                    if tmp_dev_val != None:
                        tmp_is_all_none = False
                    tmp_dev_item.append(None if tmp_dev_val == None else (round(tmp_dev_val, p_fixed_size) if p_fixed_size != None else tmp_dev_val))

                tmp_ts.append(datetime.datetime.strptime(str(tmp_item_cur_dtmi), "%Y%m%d%H%M").strftime(p_ts_format))

                # 다음 시간
                tmp_item_cur_dtmi = datetime_utils.to_int_dtmi(datetime.datetime.strptime(str(tmp_item_cur_dtmi), "%Y%m%d%H%M") + timedelta(minutes=5))

            # 다음 일자
            tmp_cur_dt = datetime_utils.to_int_dt(datetime.datetime.strptime(str(tmp_cur_dt), "%Y%m%d") + timedelta(days=1))

        return None if len(tmp_ts) == 0 else {"ts": tmp_ts, "act": tmp_act_item, "est": tmp_est_item, "dev": tmp_dev_item, "is_all_none": tmp_is_all_none}

    def get_dtmi_value(self, p_equip_id: str, p_tag_id: str, p_dtmi: int) -> float:
        tmp_cur_dt = str(p_dtmi)[:8]
        temp_value_set = None

        tmp_doc_id = "{}_{}_{}".format(p_equip_id, p_tag_id, tmp_cur_dt)
        tmp_doc_dict = self.get_as_id(tmp_doc_id)

        if tmp_doc_dict != None:
            temp_items = dict_utils.get_object(tmp_doc_dict, "items", None)
            if temp_items != None:
                temp_value_set = dict_utils.get_object(temp_items, str(p_dtmi), None)

        return temp_value_set
