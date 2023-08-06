from couchbase.collection import Collection

from skinu.core import str_utils
import skinu.sdms as sdms
from skinu.sdms.cb._base_single_document import sdmsBaseSingleDocument


#
# class sdms_meta_info
#
class sdms_meta_info:
    _meta_bucket_name = "SKADI"
    _meta_scope_name = "common"
    _meta_collection_name = "board"

    _meta_filed_dict: dict = {
        "board_id": "",
        "board_order_seq": 0,
        "written_dtmi": 190001010000,
        "written_user_id": "",
        "written_user_name": "",
        "title": "",
        "content": "",
        "readed_count": 0,
        "is_notic": False,
        "notice_post_end_dtmi": 190001010000,
        "is_deleted": False,
        "attach_file_ids": [],
        "comment_ids": [],
    }

    _meta_version: int = 1

    _meta_document_info_dict: dict = {
        "keyset": [
            {"id": "board_id", "type": "str"},
            {"id": "board_order_seq", "type": "int"},
        ],
    }

    def _request_upgrade_collection_meta_data(p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        pass


#
# class sdmsBoard
#
class sdmsBoard(sdmsBaseSingleDocument):
    def __init__(self, p_user_document_name: str = ""):
        tmp_sdms_config = sdms.sdms_get_config()
        tmp_bucket_name = sdms_meta_info._meta_bucket_name if tmp_sdms_config == None else tmp_sdms_config.bucket_name_skadi
        tmp_scope_name = sdms_meta_info._meta_scope_name
        tmp_collection_name = sdms_meta_info._meta_collection_name
        tmp_document_name = tmp_collection_name if str_utils.is_empty_str(p_user_document_name) == True else p_user_document_name
        super().__init__(tmp_bucket_name, tmp_scope_name, tmp_collection_name, tmp_document_name, None, sdms_meta_info._meta_filed_dict, sdms_meta_info._meta_version, sdms_meta_info._meta_document_info_dict, True)

    #
    # abstract method 관련
    #

    def _request_upgrade_meta_data(self, p_cb_collection: Collection, p_data_dict: dict, p_meta_verion: int, p_document_version: int) -> None:
        sdms_meta_info._request_upgrade_collection_meta_data(p_cb_collection, p_data_dict, p_meta_verion, p_document_version)
