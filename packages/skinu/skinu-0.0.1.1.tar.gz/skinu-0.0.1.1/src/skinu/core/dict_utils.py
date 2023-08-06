#
# dict 값 추출
#

def get_object(p_dict: dict, p_key: str, p_default_value: any = None) -> any:
    tmp_ret = None

    try:
        tmp_ret = p_dict[p_key]
    except:
        tmp_ret = p_default_value

    return tmp_ret


def get_str(p_dict: dict, p_key: str, p_default_value: str = "") -> str:
    tmp_ret = None

    try:
        tmp_ret = p_dict[p_key]
        if tmp_ret == None:
            tmp_ret = p_default_value
        else:
            tmp_ret = str(tmp_ret).strip()
    except:
        tmp_ret = p_default_value

    return tmp_ret


def get_int(p_dict: dict, p_key: str, p_default_value: int = None) -> int:
    tmp_ret = None

    try:
        tmp_ret = p_dict[p_key]
        tmp_ret = int(tmp_ret)
    except:
        tmp_ret = p_default_value

    return tmp_ret


def get_float(p_dict: dict, p_key: str, p_default_value: float = None) -> float:
    tmp_ret = None

    try:
        tmp_ret = p_dict[p_key]
        tmp_ret = float(tmp_ret)
    except:
        tmp_ret = p_default_value

    return tmp_ret


def get_bool(p_dict: dict, p_key: str, p_default_value: bool = None) -> bool:
    tmp_ret = None

    try:
        tmp_ret = p_dict[p_key]
        tmp_ret = bool(tmp_ret)
    except:
        tmp_ret = p_default_value

    return tmp_ret


def get_bool_from_any(p_dict: dict, p_key: str, p_default_value: bool = None) -> bool:
    tmp_ret = None

    tmp_str = get_str(p_dict, p_key, None)
    if tmp_str != None:
        tmp_ret = False

        tmp_str_len = len(tmp_str)
        if tmp_str_len == 1 or tmp_str_len == 4:
            tmp_str = tmp_str.upper()
            tmp_ret = True if tmp_str == "T" or tmp_str == "TRUE" else False
    else:
        tmp_ret = p_default_value

    return tmp_ret
