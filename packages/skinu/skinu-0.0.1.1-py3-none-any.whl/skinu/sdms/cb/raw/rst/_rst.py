import numpy as np

from couchbase.collection import Collection

import datetime as datetime
from datetime import timedelta

from skinu.core import str_utils
from skinu.core import datetime_utils
from skinu.core import dict_utils
import skinu.sdms as sdms
from skinu.sdms.cb._base_single_document import sdmsBaseSingleDocument

import pandas as PD


#
# class sdms_meta_info
#
class sdms_meta_info:
    _meta_bucket_name = "RAW"
    _meta_scope_name = "rst"
    _meta_collection_name = "rst"

    _meta_filed_dict: dict = {
        "site_id": "",
        "tag_id": "",
        "issue_dt": 19000101,
        "items": {},
        "status": {},
    }

    _meta_version: int = 1

    _meta_document_info_dict: dict = {
        "keyset": [
            {"id": "tag_id", "type": "str"},
            {"id": "issue_dt", "type": "int"},
        ],
    }

    def _request_upgrade_collection_meta_data(p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        pass


#
# class sdmsRst
#
class sdmsRst(sdmsBaseSingleDocument):
    def __init__(self, p_site_id: str = "", p_user_document_name: str = ""):
        tmp_sdms_config = sdms.sdms_get_config()
        tmp_bucket_name = sdms_meta_info._meta_bucket_name if tmp_sdms_config == None else tmp_sdms_config.bucket_name_raw
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
    def get_range_items(self, p_tag_id: str, p_from_dtimi: int, p_to_dtmi: int) -> dict:
        tmp_ret_df = PD.DataFrame()

        tmp_from_datetime = datetime.datetime.strptime(str(p_from_dtimi), "%Y%m%d%H%M")
        tmp_to_datetime = datetime.datetime.strptime(str(p_to_dtmi), "%Y%m%d%H%M")

        tmp_from_dt = datetime_utils.to_int_dt(tmp_from_datetime)
        tmp_to_dt = datetime_utils.to_int_dt(tmp_to_datetime)

        tmp_cur_dt = tmp_from_dt
        while tmp_cur_dt <= tmp_to_dt:
            tmp_doc_id = "{}_{}".format(p_tag_id, tmp_cur_dt)
            tmp_doc_dict = self.get_as_id(tmp_doc_id)
            if tmp_doc_dict != None:
                tmp_ret_df = PD.concat([tmp_ret_df, PD.DataFrame(tmp_doc_dict, columns=["items"])])

            # 다음 일자
            tmp_cur_dt = datetime_utils.to_int_dt(datetime.datetime.strptime(str(tmp_cur_dt), "%Y%m%d") + timedelta(days=1))

        tmp_ret_df = tmp_ret_df.sort_index().reset_index()
        tmp_ret_df = tmp_ret_df[tmp_ret_df["index"] >= str(p_from_dtimi)]
        tmp_ret_df = tmp_ret_df[tmp_ret_df["index"] <= str(p_to_dtmi)]
        tmp_ret_df = tmp_ret_df.set_index("index", drop=True)

        return None if tmp_ret_df.empty == True else tmp_ret_df.to_dict()

    def get_range_chart_items(self, p_tag_id: str, p_from_dtmi: int, p_to_dtmi: int, p_ts_format: str = None, p_fixed_size: int = None) -> dict:
        tmp_from_datetime = datetime.datetime.strptime(str(p_from_dtmi), "%Y%m%d%H%M")
        tmp_to_datetime = datetime.datetime.strptime(str(p_to_dtmi), "%Y%m%d%H%M")

        tmp_from_dtmi = datetime_utils.to_int_dtmi(tmp_from_datetime)
        tmp_to_dtmi = datetime_utils.to_int_dtmi(tmp_to_datetime)

        tmp_from_dt = datetime_utils.to_int_dt(tmp_from_datetime)
        tmp_to_dt = datetime_utils.to_int_dt(tmp_to_datetime)

        tmp_cur_dt = tmp_from_dt
        tmp_ts = []
        tmp_item = []
        tmp_is_all_none = True
        while tmp_cur_dt <= tmp_to_dt:
            tmp_doc_id = "{}_{}".format(p_tag_id, tmp_cur_dt)
            tmp_doc_dict = self.get_as_id(tmp_doc_id)
            tmp_item_dict = dict_utils.get_object(tmp_doc_dict, "items", None)

            tmp_item_from_dtmi = tmp_from_dtmi if tmp_cur_dt == tmp_from_dt else int(str(tmp_cur_dt) + "0000")
            tmp_item_to_dtmi = tmp_to_dtmi if tmp_cur_dt == tmp_to_dt else int(str(tmp_cur_dt) + "2359")
            tmp_item_cur_dtmi = tmp_item_from_dtmi

            while tmp_item_cur_dtmi <= tmp_item_to_dtmi:
                tmp_val = dict_utils.get_float(tmp_item_dict, str(tmp_item_cur_dtmi), None)
                if tmp_val != None:
                    tmp_is_all_none = False

                tmp_ts.append(datetime.datetime.strptime(str(tmp_item_cur_dtmi), "%Y%m%d%H%M").strftime(p_ts_format))
                tmp_item.append(None if tmp_val == None else (round(tmp_val, p_fixed_size) if p_fixed_size != None else tmp_val))

                # 다음 시간
                tmp_item_cur_dtmi = datetime_utils.to_int_dtmi(datetime.datetime.strptime(str(tmp_item_cur_dtmi), "%Y%m%d%H%M") + timedelta(minutes=1))

            # 다음 일자
            tmp_cur_dt = datetime_utils.to_int_dt(datetime.datetime.strptime(str(tmp_cur_dt), "%Y%m%d") + timedelta(days=1))

        return None if len(tmp_ts) == 0 else {"ts": tmp_ts, "act": tmp_item, "is_all_none": tmp_is_all_none}

    def get_range_min_max_mean(self, p_tag_id: str, p_from_dtimi: int, p_to_dtmi: int) -> dict:
        tmp_ret_df = PD.DataFrame()

        tmp_from_datetime = datetime.datetime.strptime(str(p_from_dtimi), "%Y%m%d%H%M")
        tmp_to_datetime = datetime.datetime.strptime(str(p_to_dtmi), "%Y%m%d%H%M")

        tmp_from_dt = datetime_utils.to_int_dt(tmp_from_datetime)
        tmp_to_dt = datetime_utils.to_int_dt(tmp_to_datetime)

        ret_dict = dict()

        tmp_cur_dt = tmp_from_dt
        while tmp_cur_dt <= tmp_to_dt:
            tmp_doc_id = "{}_{}".format(p_tag_id, tmp_cur_dt)
            tmp_doc_dict = self.get_as_id(tmp_doc_id)
            if tmp_doc_dict != None:
                tmp_ret_df = PD.concat([tmp_ret_df, PD.DataFrame(tmp_doc_dict, columns=["items"])])

            # 다음 일자
            tmp_cur_dt = datetime_utils.to_int_dt(datetime.datetime.strptime(str(tmp_cur_dt), "%Y%m%d") + timedelta(days=1))

        tmp_ret_df.index = PD.to_numeric(tmp_ret_df.index)
        tmp_ret_df.sort_index(inplace=True)
        tmp_ret_df = tmp_ret_df.loc[p_from_dtimi:p_to_dtmi]

        tmp_dict = None if tmp_ret_df.empty == True else tmp_ret_df.agg(["min", "max", "mean"]).to_dict()

        if tmp_dict != None:
            ret_dict = tmp_dict["items"]

        return ret_dict

    def get_dtmi_value(self, p_cur_dtmi: int, p_tag_id: str, p_fixed_size: int = None) -> float:
        tmp_cur_dt = str(p_cur_dtmi)[:8]
        temp_act_val = None

        tmp_doc_id = "{}_{}".format(p_tag_id, tmp_cur_dt)
        tmp_doc_dict = self.get_as_id(tmp_doc_id)

        if tmp_doc_dict != None:
            temp_items = dict_utils.get_object(tmp_doc_dict, "items", None)
            if temp_items != None:
                tmp_val = dict_utils.get_float(temp_items, str(p_cur_dtmi), None)

                # 소수점 처리
                temp_act_val = None if tmp_val == None else (round(tmp_val, p_fixed_size) if p_fixed_size != None else tmp_val)

        return temp_act_val
