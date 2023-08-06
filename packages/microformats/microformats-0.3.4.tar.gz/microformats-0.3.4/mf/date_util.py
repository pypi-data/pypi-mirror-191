"""Utility functions to deal with datetime strings."""

import datetime
import re

DATE_RE = r"(\d{4}-\d{2}-\d{2})|(\d{4}-\d{3})"
SEC_RE = r"(:(?P<second>\d{2})(\.\d+)?)"
RAWTIME_RE = rf"(?P<hour>\d{{1,2}})(:(?P<minute>\d{{2}}){SEC_RE}?)?"
AMPM_RE = r"am|pm|a\.m\.|p\.m\.|AM|PM|A\.M\.|P\.M\."
TIMEZONE_RE = r"Z|[+-]\d{1,2}:?\d{2}?"
TIME_RE = (
    rf"(?P<rawtime>{RAWTIME_RE})( ?(?P<ampm>{AMPM_RE}))?( ?(?P<tz>{TIMEZONE_RE}))?"
)
DATETIME_RE = rf"(?P<date>{DATE_RE})(?P<separator>[T ])(?P<time>{TIME_RE})"


def normalize_dt(dtstr, match=None):
    """Try to normalize a datetime string.
    1. Convert 12-hour time to 24-hour time

    pass match in if we have already calculated it to avoid rework
    """
    match = match or (dtstr and re.match(DATETIME_RE + "$", dtstr))
    if match:
        datestr = match.group("date")
        hourstr = match.group("hour")
        minutestr = match.group("minute") or "00"
        secondstr = match.group("second")
        ampmstr = match.group("ampm")
        separator = match.group("separator")

        # convert ordinal date YYYY-DDD to YYYY-MM-DD
        try:
            datestr = datetime.datetime.strptime(datestr, "%Y-%j").strftime("%Y-%m-%d")
        except ValueError:
            # datestr was not in YYYY-DDD format
            pass

        # 12 to 24 time conversion
        if ampmstr:
            hourstr = match.group("hour")
            hourint = int(hourstr)

            if (ampmstr.startswith("a") or ampmstr.startswith("A")) and hourint == 12:
                hourstr = "00"

            if (ampmstr.startswith("p") or ampmstr.startswith("P")) and hourint < 12:
                hourstr = hourint + 12

        dtstr = f"{datestr}{separator}{hourstr}:{minutestr}"

        if secondstr:
            dtstr += ":" + secondstr

        tzstr = match.group("tz")
        if tzstr:
            dtstr += tzstr
    return dtstr


def parse_dt(s):
    """The definition for microformats2 dt-* properties are fairly
    lenient.  This method converts an mf2 date string into either a
    datetime.date or datetime.datetime object. Datetimes will be naive
    unless a timezone is specified.

    :param str s: a mf2 string representation of a date or datetime
    :return: datetime.date or datetime.datetime
    :raises ValueError: if the string is not recognizable
    """

    if not s:
        return None

    s = re.sub(r"\s+", " ", s)
    date_re = r"(?P<year>\d{4,})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
    time_re = r"(?P<hour>\d{1,2}):(?P<minute>\d{2})(:(?P<second>\d{2})(\.(?P<microsecond>\d+))?)?"
    tz_re = r"(?P<tzz>Z)|(?P<tzsign>[+-])(?P<tzhour>\d{1,2}):?(?P<tzminute>\d{2})"
    dt_re = f"{date_re}((T| ){time_re} ?({tz_re})?)?$"

    m = re.match(dt_re, s)
    if not m:
        raise ValueError(f"unrecognized datetime {s}")

    year = m.group("year")
    month = m.group("month")
    day = m.group("day")

    hour = m.group("hour")

    if not hour:
        return datetime.date(int(year), int(month), int(day))

    minute = m.group("minute") or "00"
    second = m.group("second") or "00"

    if hour:
        dt = datetime.datetime(
            int(year), int(month), int(day), int(hour), int(minute), int(second)
        )
    if m.group("tzz"):
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    else:
        tzsign = m.group("tzsign")
        tzhour = m.group("tzhour")
        tzminute = m.group("tzminute") or "00"

        if tzsign and tzhour:
            offset = datetime.timedelta(hours=int(tzhour), minutes=int(tzminute))
            if tzsign == "-":
                offset = -offset
            dt = dt.replace(
                tzinfo=datetime.timezone(offset, f"{tzsign}{tzhour}:{tzminute}")
            )

    return dt
