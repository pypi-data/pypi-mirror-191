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
    YEAR1 = 12 * MON1

    def _get_1m_timeframes(self):
        return [
            self.MIN1,
            self.MIN3,
            self.MIN5,
            self.MIN15,
            self.MIN30,
            self.HOUR1,
            self.HOUR2,
            self.HOUR4,
            self.HOUR6,
            self.HOUR8,
            self.HOUR12,
            self.DAY1,
            self.DAY3,
            self.WEEK1,
            self.MON1,
            self.YEAR1,
        ]

    def _get_1h_timeframes(self):
        return [
            self.HOUR1,
            self.HOUR2,
            self.HOUR4,
            self.HOUR6,
            self.HOUR8,
            self.HOUR12,
            self.DAY1,
            self.DAY3,
            self.WEEK1,
            self.MON1,
            self.YEAR1,
        ]
    
    def _get_1d_timeframes(self):
        return [
            self.DAY1,
            self.DAY3,
            self.WEEK1,
            self.MON1,
            self.YEAR1,
        ]