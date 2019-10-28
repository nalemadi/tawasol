from datetime import datetime, timedelta
from ..config.dashboard_config import TIME_GRANULARITY, TIME_COVERED


class TimeAnalyzer:

    def __init__(self):
        self.datetime_formatter = '%Y-%m-%dT%H:%M'

    def to_datetime(self, created_at):
        """
        convert string to date
        :param created_at: string
        :return: datetime
        """
        dt = datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y')
        dt = dt.replace(second=0, microsecond=0)
        return dt

    def date_generator(self, start_date, end_date):
        """
        time generator with granularity min_timedelta between start and end date
        :param start_date:
        :param end_date:
        :return: list
        """
        delta = timedelta(minutes=1)
        current_date = start_date
        while current_date < end_date:
            yield current_date
            current_date += delta

    def convert_datetime_toString(self, dtime):
        """
        convert datetime to string with format formatter
        :param dtime:
        :param formatter: date formatter
        :return: string
        """
        return dtime.strftime('%Y-%m-%dT%H:%M')

    def convert_timestamp_toDatetime(self, timestamp):
        """
        convert timestamp(int) to datetime
        :param timestamp: integer
        :return: datetime
        """
        return datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y-%m-%dT%H:%M')

    def convert_time_to_timeslot(self, dt, time_slots):
        for i in range(0,len(time_slots)-1):
            next_time_slot = time_slots[i+1]
            curr_time_slot = time_slots[i]
            if curr_time_slot <= dt and dt < next_time_slot:
                return curr_time_slot.strftime('%Y-%m-%dT%H:%M')
                break
        return None

    def get_all_timeslots(self):
        """
        prepare timeslots list
        :return: timeslots list
        """
        max_frames = TIME_COVERED
        start = datetime.utcnow()
        time_slots = [start - timedelta(minutes=x) for x in range(0, max_frames+1, TIME_GRANULARITY)]
        return sorted(time_slots)

    # def get_time_index(self, dt, time_slots):
    # 	for i in range(0, len(time_slots) - 1):
    # 		next_time_slot = time_slots[i + 1]
    # 		curr_time_slot = time_slots[i]
    # 		if curr_time_slot <= dt and dt < next_time_slot:
    # 			return curr_time_slot.strftime('%Y-%m-%dT%H:%M')
    # 	return None

    def get_accounts_creation_ranges(self):
        self.current_date = datetime.now().date()
        self.week_ago = self.current_date - timedelta(days=7)
        self.month_age = self.current_date - timedelta(days=30)
        self.months_3_ago = self.current_date - timedelta(days=90)
        self.months_6_ago = self.current_date - timedelta(days=180)
        self.year_ago = self.current_date - timedelta(days=365)

    def get_time_index(self, tweet_date, time_slots):
        """
        :param tweet_date:
        :param time_slots:
        :return:
        """
        for curr_time_slot, next_time_slot in zip(time_slots, time_slots[1:]):
            if curr_time_slot <= tweet_date < next_time_slot:
                return curr_time_slot.strftime('%Y-%m-%dT%H:%M')
        return None

    def get_account_creation_cat(self, creation_date_st):
        range = '+Year'
        creation_date = datetime.strptime(creation_date_st, '%a %b %d %H:%M:%S +0000 %Y').date()
        if self.week_ago <= creation_date:
            range = 'Week'
        elif self.month_age <= creation_date:
            range = 'Month'
        elif self.months_3_ago <= creation_date:
            range = '3-Months'
        elif self.months_6_ago <= creation_date:
            range = '6-Months'
        elif self.year_ago <= creation_date:
            range = 'Year'
        elif creation_date < self.year_ago:
            range = '+Year'
        else:
            print 'error in get_account_creation_range'
        return range
