#
# pandas 객체 문자열로 변환
#

def to_trim_str(p_var: any, p_default_val: str = "", p_ignore_str: str = 'x') -> str:
    import pandas as PD

    p_var = p_default_val if p_var == None or PD.isnull(p_var) == True else str(p_var).strip()
    p_var = p_default_val if p_var == None or len(p_var) == 0 else p_var

    if p_var != None and len(p_var) == 1 and (p_var == p_ignore_str.lower() or p_var == p_ignore_str.upper()):
        p_var = ""

    return p_var


def to_trim_int(p_var: any, p_default_val: int = 0) -> int:
    p_var = to_trim_str(p_var, None)

    try:
        p_var = p_default_val if p_var == None or len(p_var) == 0 else int(float(p_var))
    except:
        p_var = p_default_val

    return p_var


def to_trim_float(p_var: any, p_default_val: float = 0.0) -> float:
    p_var = to_trim_str(p_var, None)
    try:
        p_var = p_default_val if p_var == None or len(p_var) == 0 else float(p_var)
    except:
        p_var = p_default_val

    return p_var


def to_trim_bool(p_var: any, p_default_val: bool = False) -> bool:
    p_var = to_trim_str(p_var, None)
    try:
        if p_var == None or len(p_var) == 0:
            p_var = p_default_val
        else:
            if p_var == "0" or p_var.upper() == 'F' or p_var.upper() == 'FALSE':
                p_var = True
            else:
                p_var = False
    except:
        p_var = p_default_val

    return p_var
