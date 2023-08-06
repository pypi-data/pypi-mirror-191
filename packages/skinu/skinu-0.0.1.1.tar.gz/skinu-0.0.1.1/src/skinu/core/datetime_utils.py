import datetime as datetime

#
# datetime -> init
#


def to_int_fmt(p_datetime: datetime.datetime, p_format: str, p_suffix_str: str = "") -> int:
    tmp_str_fmt_datetime = p_datetime.strftime(p_format) + p_suffix_str
    return int(tmp_str_fmt_datetime)


def to_int_datetime(p_datetime: datetime.datetime, p_suffix_str: str = "") -> int:
    return to_int_fmt(p_datetime, "%Y%m%d%H%M%S", p_suffix_str)


def to_int_date(p_datetime: datetime.datetime, p_suffix_str: str = "") -> int:
    return to_int_fmt(p_datetime, "%Y%m%d", p_suffix_str)


def to_int_time(p_datetime: datetime.datetime, p_suffix_str: str = "") -> int:
    return to_int_fmt(p_datetime, "%H%M%S", p_suffix_str)


def to_int_dt(p_datetime: datetime.datetime, p_suffix_str: str = "") -> int:
    return to_int_fmt(p_datetime, "%Y%m%d", p_suffix_str)


def to_int_dth(p_datetime: datetime.datetime, p_suffix_str: str = "") -> int:
    return to_int_fmt(p_datetime, "%Y%m%d%H", p_suffix_str)


def to_int_dtmi(p_datetime: datetime.datetime, p_suffix_str="") -> int:
    return to_int_fmt(p_datetime, "%Y%m%d%H%M", p_suffix_str)


def to_int_ym(p_datetime: datetime.datetime, p_suffix_str: str = "") -> int:
    return to_int_fmt(p_datetime, "%Y%m", p_suffix_str)


def to_int_ymd(p_datetime: datetime.datetime, p_suffix_str: str = "") -> int:
    return to_int_fmt(p_datetime, "%Y%m%d", p_suffix_str)


def to_int_hms(p_datetime: datetime.datetime, p_suffix_str: str = "") -> int:
    return to_int_fmt(p_datetime, "%H%M%S", p_suffix_str)


def to_int_tm(p_datetime: datetime.datetime, p_suffix_str: str = "") -> int:
    return to_int_fmt(p_datetime, "%Y%m%d%H%M%S", p_suffix_str)
