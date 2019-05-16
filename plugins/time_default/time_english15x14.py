""" Provided by Alexandre"""


class time_english:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on an english WCA
    """

    def __init__(self):
        self.prefix = range(0,3) +  range(5, 9) + range(11, 13) # -> THE TIME IS
        self.about = range(16,21)
        self.minutes_past = range(76,83) + range(85, 89) 
        self.am = range(159, 161)
        self.pm = range(162, 164)
        self.time_for = range(165, 169) + range(175, 178)
        self.coffee = range(180, 186)
        self.lunch = range(186, 191)
        self.tea = range(192, 195)
        self.whiskey = range(195, 202)
        self.time_to_go_home = range(165, 169) + range(171, 173) + range(203, 205) + range(206, 210)

        self.minutes=[[], \
            # -> FIVE 
            range(67, 71), \
            # -> TEN
            range(23, 26), \
            # -> QUARTER PAST
            range(30, 37), \
            # -> TWENTY PAST
            range(45, 51), \
            # -> TWENTYFIVE PAST
            range(45, 51) + range(67, 71), \
            # -> THIRTY
            range(52, 58), \
            # -> THIRTY FIVE
            range(52, 58) + range(67, 71), \
            # -> FORTY
            range(39, 44), \
            # -> FORTY FIVE
            range(39, 44) + range(67, 71), \
            # -> FIFTY
            range(60, 65), \
            # -> FIFTY FIVE
            range(60, 65) + range(67, 71) ]
            # -> TWELVE
        self.hours= [range(144, 150), \
            # -> ONE
            range(90, 93), \
            # -> TWO
            range(94, 97), \
            # -> THREE
            range(99, 104), \
            # -> FOUR
            range(105, 109), \
            # -> FIVE
            range(109, 113), \
            # -> SIX
            range(135, 138), \
            # -> SEVEN
            range(139, 144), \
            # -> EIGHT
            range(121, 126), \
            # -> NINE
            range(127, 131), \
            # -> TEN
            range(132, 135),\
            # -> ELEVEN
            range(114 ,120), \
            # -> TWELVE
            range(144, 150)]
        # -> OCLOCK
        self.full_hour= range(151, 157)

    def get_time(self, time, purist):
        hour=time.hour % 12
        minute=time.minute/5

        # Assemble indices
        ret = []
        ret.extend(self.prefix)
        if (time.minute % 5) != 0:
            ret.extend(self.about)
        if minute > 0:
            ret.extend(self.minutes[minute])
            ret.extend(self.minutes_past)
        ret.extend(self.hours[hour])
        if minute == 0:
            ret.extend(self.full_hour)
        if time.hour > 11:
            ret.extend(self.pm)
        else:
            ret.extend(self.am)
        # Weekdays
        if time.weekday() <= 4:
            # time for coffee 
            if time.hour == 10 and time.minute >= 0 and time.minute <= 10:
                ret.extend(self.time_for + self.coffee)
            if time.hour == 12:
                ret.extend(self.time_for + self.lunch)
            if time.hour == 15 and time.minute >= 0 and time.minute <= 10:
                ret.extend(self.time_for + self.tea)
            if time.hour == 16:
                ret.extend(self.time_for + self.whiskey)
        #print ret
        return ret

