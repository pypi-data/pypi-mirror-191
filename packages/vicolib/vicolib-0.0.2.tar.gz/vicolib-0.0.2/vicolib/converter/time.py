import datetime

formats = {
    "def": "%Y/%m/%d - %X",
    "dmy": "%d.%m.%Y",
    "dmy-time": "%d.%m.%Y - %X",
    "ymd": "%Y/%m%d",
    "ymd-time": "%Y/%m/%d - %X",
    "time": "%H:%M",
    "time-s": "%X",
    "time-apm": "%I:%M %p",
    "written": "%A %d. %B %Y",
}


class Time:
    """
    Time methods:
    Time.stamp_now()
    # Converts the current time to a formattable timestamp string
    # ? params: format: string -> e.g. "%Y/%m/%d" or from formats dict:
        "def": "%Y/%m/%d - %X",         -> 2023/2/4 - 18:30:26
        "dmy": "%d.%m.%Y",              -> 4.2.2023
        "dmy-time": "%d.%m.%Y - %X",    -> 4.2.2023 - 18:30:26
        "ymd": "%Y/%m%d",               -> 2023/2/4
        "ymd-time": "%Y/%m/%d - %X",    -> 2023/2/4 - 18:30:26
    # ? return: str (like "2023/2/4 - 18:30:26")
    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Time, cls).__new__(cls)
        return cls.instance

    @staticmethod
    # Converts the current time to a formattable timestamp string
    def stamp_now(format: str = "") -> str:
        global formats
        now = datetime.datetime.now()

        if not format:
            format = formats["def"]
        if format in formats:
            format = formats[format]
        return now.strftime(format)


    # Converts microseconds (us) to milliseconds (ms).
    @staticmethod
    def us_to_ms(us):
        if type(us) is str:
            if us.isdigit():
                us = int(us)
            else:
                raise ValueError(
                    f"Could not convert '{us}' microseconds to milliseconds!"
                )
        return round(us / 1000)

    # Converts milliseconds (ms) to microseconds (us).
    @staticmethod
    def ms_to_us(ms):
        if type(ms) is str:
            if ms.isdigit():
                ms = int(ms)
            else:
                raise ValueError(
                    f"Could not convert '{ms}' milliseconds to microseconds!"
                )
        return int(ms * 1000)
