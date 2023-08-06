#
# class sdmsConfig
#
class sdmsConfig:
    # 생성자
    def __init__(self, p_mode: str):
        self.__mode = p_mode

        #
        # couchbase 설정 정보
        #
        self.__couchbase_set = {
            "product": {
                "username": "ia00655",
                "password": "1q2w3e4r",
                "endpoint": "10.78.236.19",
                "connection_timeout": 10,

                "bucket_name_raw": "RAW",
                "bucket_name_raw_eai": "RAW_EAI",
                "bucket_name_est": "EST",
                "bucket_name_ref": "REF",
                "bucket_name_skadi": "SKADI",
                "bucket_name_worklog": "WORKLOG",
                "bucket_name_message": "MESSAGE",
            },

            "test": {
                "username": "ia00655",
                "password": "1q2w3e4r",
                "endpoint": "168.154.132.172",
                "connection_timeout": 10,

                "bucket_name_raw": "RAW",
                "bucket_name_raw_eai": "RAW_EAI",
                "bucket_name_est": "EST",
                "bucket_name_ref": "REF",
                "bucket_name_skadi": "SKADI",
                "bucket_name_worklog": "WORKLOG",
                "bucket_name_message": "MESSAGE",
            },

            "dev": {
                "username": "root",
                "password": "Temp5dmin##",
                "endpoint": "web-0.manager.couchbase.svc.cluster.local",
                "connection_timeout": 10,

                "bucket_name_raw": "C_RAW",
                "bucket_name_raw_eai": "C_RAW_EAI",
                "bucket_name_est": "C_EST",
                "bucket_name_ref": "C_REF",
                "bucket_name_skadi": "C_SKADI",
                "bucket_name_worklog": "C_WORKLOG",
                "bucket_name_message": "C_MESSAGE",
            },

        }

    # =================================
    # couchbase 설정 정보
    # =================================
    @property
    def username(self) -> str:
        return self._get_property(self.__couchbase_set, "username")

    @property
    def password(self) -> str:
        return self._get_property(self.__couchbase_set, "password")

    @property
    def endpoint(self) -> str:
        return self._get_property(self.__couchbase_set, "endpoint")

    @property
    def connection_timeout(self) -> int:
        return self._get_property(self.__couchbase_set, "connection_timeout")

    # =================================
    # bucket 명칭
    # =================================
    @property
    def bucket_name_raw(self) -> str:
        return self._get_property(self.__couchbase_set, "bucket_name_raw")

    @property
    def bucket_name_raw_eai(self) -> str:
        return self._get_property(self.__couchbase_set, "bucket_name_raw_eai")

    @property
    def bucket_name_est(self) -> str:
        return self._get_property(self.__couchbase_set, "bucket_name_est")

    @property
    def bucket_name_ref(self) -> str:
        return self._get_property(self.__couchbase_set, "bucket_name_ref")

    @property
    def bucket_name_skadi(self) -> str:
        return self._get_property(self.__couchbase_set, "bucket_name_skadi")

    @property
    def bucket_name_worklog(self) -> str:
        return self._get_property(self.__couchbase_set, "bucket_name_worklog")

    @property
    def bucket_name_message(self) -> str:
        return self._get_property(self.__couchbase_set, "bucket_name_message")

    # =================================
    # 내부 함수
    # =================================
    def _get_property(self, p_data_dict: dict, key: str) -> any:
        try:
            return (p_data_dict["common"])[key]
        except:
            if self.__mode == "test" or self.__mode == "product":
                return (p_data_dict[self.__mode])[key]
            else:
                return (p_data_dict["dev"])[key]
