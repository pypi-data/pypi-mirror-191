from datetime import date, timedelta
from dataclasses import dataclass

RELEASE_DAY_OF_WEEK = 2  # Wednesday, datetime starts from 0
NUM_DAYS_OF_WEEK = 7


@dataclass(init=False)
class ReleaseDay:
    def __init__(self, _date: date = None):
        if _date:
            start_date = _date
        else:
            start_date = date.today()
        self.release_date = start_date + timedelta((RELEASE_DAY_OF_WEEK -
                                                    start_date.weekday()) %
                                                   NUM_DAYS_OF_WEEK)
