import sys
import logging
import colorlog


#
# class _skinuLog
#
class _skinuLog():
    __Logger: logging.Logger = None

    @staticmethod
    def init():
        _skinuLog.__Logger = logging.getLogger("PY-SKINU")

        # 포맷터 설정
        tmp_date_fmt = "%Y-%m-%d %H:%M:%S"
        tmp_stream_formatter = colorlog.ColoredFormatter("%(asctime)s %(log_color)s[%(levelname)-8s]%(reset)s [%(name)s] [%(module)s:%(lineno)d] : %(message)s", datefmt=tmp_date_fmt)

        # 핸들러 설정
        tmp_stream_hander = colorlog.StreamHandler(sys.stdout)

        # Console 포맷터 설정 및 인스턴스 추가
        tmp_stream_hander.setFormatter(tmp_stream_formatter)
        _skinuLog.__Logger.addHandler(tmp_stream_hander)

        # loger 설정
        _skinuLog.__Logger.setLevel(logging.NOTSET)

    @staticmethod
    def getLogger() -> logging.Logger:
        return _skinuLog.__Logger


#
# init
#
_skinuLog.init()
