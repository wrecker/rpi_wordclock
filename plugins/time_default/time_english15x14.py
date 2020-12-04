""" Provided by Alexandre"""


class time_english:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on an english WCA
    """

    def __init__(self):
        self.prefix = list(range(0,3)) +  list(range(5, 9)) + list(range(11, 13)) # -> THE TIME IS
        self.about = list(range(16,21))
        self.minutes_past = list(range(76,83)) + list(range(85, 89))
        self.am = list(range(159, 161))
        self.pm = list(range(162, 164))
        self.time_for = list(range(165, 169)) + list(range(175, 178))
        self.coffee = list(range(180, 186))
        self.lunch = list(range(186, 191))
        self.tea = list(range(192, 195))
        self.whiskey = list(range(195, 202))
        self.time_to_go_home = list(range(165, 169)) + list(range(171, 173)) + list(range(203, 205)) + list(range(206, 210))

        self.minutes=[[], \
            # -> FIVE 
            list(range(67, 71)), \
            # -> TEN
            list(range(23, 26)), \
            # -> QUARTER PAST
            list(range(30, 37)), \
            # -> TWENTY PAST
            list(range(45, 51)), \
            # -> TWENTYFIVE PAST
            list(range(45, 51)) + list(range(67, 71)), \
            # -> THIRTY
            list(range(52, 58)), \
            # -> THIRTY FIVE
            list(range(52, 58)) + list(range(67, 71)), \
            # -> FORTY
            list(range(39, 44)), \
            # -> FORTY FIVE
            list(range(39, 44)) + list(range(67, 71)), \
            # -> FIFTY
            list(range(60, 65)), \
            # -> FIFTY FIVE
            list(range(60, 65)) + list(range(67, 71)) ]
            # -> TWELVE
        self.hours= [list(range(144, 150)), \
            # -> ONE
            list(range(90, 93)), \
            # -> TWO
            list(range(94, 97)), \
            # -> THREE
            list(range(99, 104)), \
            # -> FOUR
            list(range(105, 109)), \
            # -> FIVE
            list(range(109, 113)), \
            # -> SIX
            list(range(135, 138)), \
            # -> SEVEN
            list(range(139, 144)), \
            # -> EIGHT
            list(range(121, 126)), \
            # -> NINE
            list(range(127, 131)), \
            # -> TEN
            list(range(132, 135)),\
            # -> ELEVEN
            list(range(114 ,120)), \
            # -> TWELVE
            list(range(144, 150))]
        # -> OCLOCK
        self.full_hour= list(range(151, 157))

    def get_time(self, time, purist):
        hour=time.hour % 12
        minute=int(time.minute/5)
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

