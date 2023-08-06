#
# 빈 문자열 여부 검사
#

def is_empty_str(p_str: str) -> bool:
    try:
        if p_str == None or len(p_str.strip()) == 0:
            return True
    except:
        return False

    return False


def is_not_empty_str(p_str: str) -> bool:
    return False if is_empty_str(p_str) == True else True


#
# 문자열로 변환
#

def to_trim_str(p_var: any, p_default_val: str = "") -> str:
    if p_var == None:
        return p_default_val

    return str(p_var).strip()


def to_trim_int(p_var: any, p_default_val: int = 0) -> int:
    p_var = to_trim_str(p_var)

    try:
        p_var = p_default_val if p_var == None or len(p_var) == 0 else int(p_var)
    except:
        p_var = p_default_val

    return p_var


def to_trim_float(p_var: any, p_default_val: float = 0) -> float:
    p_var = to_trim_str(p_var)

    try:
        p_var = p_default_val if p_var == None or len(p_var) == 0 else float(p_var)
    except:
        p_var = p_default_val

    return p_var


def to_trim_bool(p_var: any, p_default_val: bool = False) -> bool:
    p_var = to_trim_str(p_var)

    try:
        if p_var == None or len(p_var) == 0:
            p_var = p_default_val
        else:
            if p_var == "0" or p_var.upper() == 'F' or p_var.upper() == 'FALSE':
                p_var = False
            else:
                p_var = True
    except:
        p_var = p_default_val

    return p_var
