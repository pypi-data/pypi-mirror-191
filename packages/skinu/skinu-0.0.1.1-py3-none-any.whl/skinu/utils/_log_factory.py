import os
import sys
from logging import handlers
import logging
import colorlog


#
# class LogFactory
#
class LogFactory:
    __Logger: logging.Logger = None

    @staticmethod
    def init(p_log_name: str = "", p_log_level: str = "INFO", p_log_path: str = None, p_file_name: str = None, p_backup_count: int = 15, p_backup_max_size_mb=100, p_encoding: str = "utf-8") -> None:
        tmp_log_is_output_file = False

        # 로그 파일 경로 생성
        if (p_log_path != None) and (len(p_log_path) > 0):
            tmp_log_is_output_file = True

            if os.path.exists(p_log_path) == False:
                try:
                    os.makedirs(p_log_path)
                except OSError as e:
                    tmp_log_is_output_file = False

        # 파일 출력 여부
        if (tmp_log_is_output_file == True) and ((p_file_name == None) or (len(p_file_name) == 0)):
            tmp_log_is_output_file = False

        # 로그 인스턴스 생성
        LogFactory.__Logger = logging.getLogger(p_log_name)

        # 포맷터 설정
        tmp_date_fmt = "%Y-%m-%d %H:%M:%S"
        tmp_stream_formatter = colorlog.ColoredFormatter("%(asctime)s %(log_color)s[%(levelname)-8s]%(reset)s [%(name)s] [%(module)s:%(lineno)d] : %(message)s", datefmt=tmp_date_fmt)

        # 핸들러 설정
        tmp_stream_hander = colorlog.StreamHandler(sys.stdout)

        # Console 포맷터 설정 및 인스턴스 추가
        tmp_stream_hander.setFormatter(tmp_stream_formatter)
        LogFactory.__Logger.addHandler(tmp_stream_hander)

        # File 포맷터 설정 및 인스턴스 추가
        if tmp_log_is_output_file == True:
            tmp_file_formatter = logging.Formatter("%(asctime)s [%(levelname)-8s] [%(name)s] [%(module)s:%(lineno)d] : %(message)s", datefmt=tmp_date_fmt)

            tmp_file_handler = handlers.RotatingFileHandler(
                os.path.abspath(f"{p_log_path}f{p_file_name}.log"),
                mode='a',
                maxBytes=(1024 * 1024 * p_backup_max_size_mb),
                backupCount=p_backup_count,
                encoding=p_encoding)

            tmp_file_handler.setFormatter(tmp_file_formatter)
            LogFactory.__Logger.addHandler(tmp_file_handler)

        # 로그 레벨 설정
        p_log_level = p_log_level.upper()
        if p_log_level == "CRITICAL":
            LogFactory.__Logger.setLevel(logging.CRITICAL)
        elif p_log_level == "FATAL":
            LogFactory.__Logger.setLevel(logging.FATAL)
        elif p_log_level == "ERROR":
            LogFactory.__Logger.setLevel(logging.ERROR)
        elif p_log_level == "WARNING":
            LogFactory.__Logger.setLevel(logging.WARNING)
        elif p_log_level == "INFO":
            LogFactory.__Logger.setLevel(logging.INFO)
        elif p_log_level == "DEBUG":
            LogFactory.__Logger.setLevel(logging.DEBUG)

    @staticmethod
    def getLogger() -> logging.Logger:
        return LogFactory.__Logger

    @staticmethod
    def is_init() -> bool:
        return True if LogFactory.__Logger != None else False
