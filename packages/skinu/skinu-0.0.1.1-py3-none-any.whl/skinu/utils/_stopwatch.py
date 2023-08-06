import time as time


#
# class stopwatch
#
class Stopwatch:
    def __init__(self):
        self.__is_start = False
        self.__start_tm = 0
        self.__stop_tm = 0

    def start(self) -> None:
        if self.__is_start == False:
            self.__start_tm = time.time()
            self.__stop_tm = self.__start_tm

        self.__is_start = True

    def stop(self) -> None:
        if self.__is_start == True:
            self.__stop_tm = time.time()

        self.__is_start = False

    @property
    def eslimatedSeconds(self) -> str:
        tmp_elimated_time = 0

        if self.__is_start == True:
            tmp_elimated_time = time.time() - self.__start_tm
        else:
            tmp_elimated_time = self.__stop_tm - self.__start_tm

        return "%.2f" % tmp_elimated_time
