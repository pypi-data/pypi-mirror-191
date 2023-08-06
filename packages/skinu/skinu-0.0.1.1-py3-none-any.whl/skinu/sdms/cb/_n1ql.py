import skinu.sdms as sdms
from skinu.core import dict_utils

from couchbase.options import QueryOptions
from couchbase.n1ql import QueryScanConsistency
from couchbase.result import QueryResult

import pandas as pd

from skinu._internal._logs import _skinuLog


class sdmsQueryOptions:
    FAST_SCAN = QueryOptions(scan_consistency=QueryScanConsistency.NOT_BOUNDED)
    FULL_SCAN = QueryOptions(scan_consistency=QueryScanConsistency.REQUEST_PLUS)


class sdmsN1ql:
    #
    # 자주 사용되는 쿼리
    #

    @staticmethod
    def _get_default_parameters() -> dict:
        tmp_sdms_config = sdms.sdms_get_config()

        tmp_params = {
            "P_RAW_BUCKET": tmp_sdms_config.bucket_name_raw,
            "P_RAW_EAI_BUCKET": tmp_sdms_config.bucket_name_raw_eai,
            "P_EST_BUCKET": tmp_sdms_config.bucket_name_est,
            "P_REF_BUCKET": tmp_sdms_config.bucket_name_ref,
            "P_SKADI_BUCKET": tmp_sdms_config.bucket_name_skadi,
            "P_WORKLOG_BUCKET": tmp_sdms_config.bucket_name_worklog,
            "P_MESSAGE_BUCKET": tmp_sdms_config.bucket_name_message,

            "p_raw_bucket": tmp_sdms_config.bucket_name_raw,
            "p_raw_eai_bucket": tmp_sdms_config.bucket_name_raw_eai,
            "p_est_bucket": tmp_sdms_config.bucket_name_est,
            "p_ref_bucket": tmp_sdms_config.bucket_name_ref,
            "p_skadi_bucket": tmp_sdms_config.bucket_name_skadi,
            "p_worklog_bucket": tmp_sdms_config.bucket_name_worklog,
            "p_message_bucket": tmp_sdms_config.bucket_name_message,
        }

        return tmp_params

    @staticmethod
    def select_count(query: str, query_option: QueryOptions = None, **kwargs) -> int:
        tmp_cnt = 0

        # 기본 파라미터
        tmp_params = sdmsN1ql._get_default_parameters()

        # 쿼리 생성
        tmp_query = query.format(**tmp_params, **kwargs)

        _skinuLog.getLogger().info(tmp_query)

        # 쿼리 실행
        tmp_cluster = sdms.sdms_get_cluster()

        tmp_result = None
        if query_option == None:
            tmp_result = tmp_cluster.query(tmp_query)
        else:
            tmp_result = tmp_cluster.query(tmp_query, query_option)

        for tmp_record in tmp_result.rows():
            tmp_cnt = dict_utils.get_int(tmp_record, "cnt", None)
            if tmp_cnt == None:
                tmp_cnt = dict_utils.get_int(tmp_record, "CNT", 0)

        return tmp_cnt

    @staticmethod
    def select_list(query: str, query_option: QueryOptions = None, **kwargs) -> pd.DataFrame:
        # 기본 파라미터
        tmp_params = sdmsN1ql._get_default_parameters()

        # 쿼리 생성
        tmp_query = query.format(**tmp_params, **kwargs)

        _skinuLog.getLogger().info(tmp_query)

        # 쿼리 실행
        tmp_cluster = sdms.sdms_get_cluster()

        tmp_records = None
        if query_option == None:
            tmp_records = tmp_cluster.query(tmp_query)
        else:
            tmp_records = tmp_cluster.query(tmp_query, query_option)

        # DataFrame 으로 변환
        tmp_pandas = pd.DataFrame(tmp_records.rows())

        return tmp_pandas

    @staticmethod
    def select_result(query: str, query_option: QueryOptions = None, **kwargs) -> QueryResult:
        # 기본 파라미터
        tmp_params = sdmsN1ql._get_default_parameters()

        # 쿼리 생성
        tmp_query = query.format(**tmp_params, **kwargs)

        _skinuLog.getLogger().info(tmp_query)

        # 쿼리 실행
        tmp_cluster = sdms.sdms_get_cluster()

        tmp_records = None
        if query_option == None:
            tmp_records = tmp_cluster.query(tmp_query)
        else:
            tmp_records = tmp_cluster.query(tmp_query, query_option)

        return tmp_records

    @staticmethod
    def select_page_list(query: str, page_num: int, page_length: int, query_option: QueryOptions = None, **kwargs) -> pd.DataFrame:
        # 기본 파라미터
        tmp_params = sdmsN1ql._get_default_parameters()

        # 추가 파라미터
        tmp_params["P_LIMIT"] = page_length
        tmp_params["P_OFFSET"] = (int(page_num) - 1) * (int(page_length))

        tmp_params["p_limit"] = page_length
        tmp_params["p_offset"] = (int(page_num) - 1) * (int(page_length))

        # 쿼리 생성
        tmp_query = query.format(**tmp_params, **kwargs)

        _skinuLog.getLogger().info(tmp_query)

        # 쿼리 실행
        tmp_cluster = sdms.sdms_get_cluster()

        tmp_records = None
        if query_option == None:
            tmp_records = tmp_cluster.query(tmp_query)
        else:
            tmp_records = tmp_cluster.query(tmp_query, query_option)

        # DataFrame 으로 변환
        tmp_pandas = pd.DataFrame(tmp_records.rows())

        return tmp_pandas

    @staticmethod
    async def async_select_count(key: str, query: str, query_option: QueryOptions = None, **kwargs) -> dict:
        tmp_ret_cnt = sdmsN1ql.select_count(query, query, query_option, **kwargs)

        return {"key": key, "count": tmp_ret_cnt}

    @staticmethod
    async def async_select_list(key: str, query: str, query_option: QueryOptions = None, **kwargs) -> dict:
        tmp_ret_list = sdmsN1ql.select_list(str, query, query_option, **kwargs)

        return {"key": key, "dataframe": tmp_ret_list}

    @staticmethod
    async def async_select_result(key: str, query: str, query_option: QueryOptions = None, **kwargs) -> dict:
        tmp_ret_result = sdmsN1ql.select_result(str, query, query_option, **kwargs)

        return {"key": key, "result": tmp_ret_result}

    @staticmethod
    async def async_select_page_list(key: str, query: str, page_num: int, page_length: int, query_option: QueryOptions = None, **kwargs) -> dict:
        tmp_ret_list = sdmsN1ql.select_page_list(query, page_num, page_length, query_option, **kwargs)

        return {"key": key, "page_num": page_num, "page_length": page_length, "dataframe": tmp_ret_list}
