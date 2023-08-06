class Interval:
    MIN1 = 60
    MIN3 = 3 * MIN1
    MIN5 = 5 * MIN1
    MIN15 = 15 * MIN1
    MIN30 = 30 * MIN1
    HOUR1 = 60 * MIN1
    HOUR2 = 2 * HOUR1
    HOUR4 = 4 * HOUR1
    HOUR6 = 6 * HOUR1
    HOUR8 = 8 * HOUR1
    HOUR12 = 12 * HOUR1
    DAY1 = 24 * HOUR1
    DAY3 = 3 * DAY1
    WEEK1 = 7 * DAY1
    MON1 = 30 * DAY1

    @staticmethod
    def get_str(interval) -> str:
        seconds = interval
        if seconds < 60:
            return "{}s".format(seconds)

        minute = int(seconds / 60)
        if minute < 60:
            return "{}m".format(minute)

        hour = int(minute / 60)
        if hour < 24:
            return "{}H".format(hour)

        day = int(hour / 24)
        if day < 7:
            return "{}D".format(day)

        week = int(day / 7)
        if week < 4:
            return "{}W".format(week)

        return "1M"
