import re


months = [
    'afteryule',
    'solmath',
    'rethe',
    'astron',
    'thrimidge',
    'forelithe',
    'afterlithe',
    'wedmath',
    'halimath',
    'winterfilth',
    'blotmath',
    'foreyule',
]

holiday_months = [
    'yule',
    'lithe',
]

holidays = [
    'mid-year\'s day',
    'overlithe',
]


# Year/month/day helpers

def is_leap_year(year):
    return year % 4 == 0 and year % 100 > 0


def get_days_in_year(year):
    return 366 if is_leap_year(year) else 365


def month_from_day_of_year(day_index, year):
    days_in_year = get_days_in_year(year)
    leap_year = is_leap_year(year)

    if day_index < 1 or day_index > days_in_year:
        raise Exception('Invalid day of year')

    if day_index in [1, days_in_year]:
        return 'yule'
    elif day_index in [182, (185 if leap_year else 184)]:
        return 'lithe'
    elif day_index == 183:
        return 'mid-year\'s day'
    elif day_index == 184 and leap_year:
        return 'overlithe'
    else:
        holiday_count = 1 + (0 if day_index < 182 else (4 if leap_year else 3))
        return months[(day_index - holiday_count + 29) // 30 - 1]


def day_of_month_from_day_of_year(day_index, year):
    days_in_year = get_days_in_year(year)
    leap_year = is_leap_year(year)

    if day_index < 1 or day_index > days_in_year:
        raise Exception('Invalid day of year')

    if day_index in [182, 183, days_in_year] or (day_index == 184 and leap_year):
        return 1
    elif day_index in [1, (185 if leap_year else 184)]:
        return 2
    else:
        holiday_count = 1 + (0 if day_index < 182 else (4 if leap_year else 3))
        return (day_index - holiday_count - 1) % 30 + 1


# String helpers

def title_case(string):
    return re.sub('[-A-Za-z]+(?:\'[-A-Za-z]+)?',
                  lambda m: m.group(0)[0].upper() + m.group(0)[1:].lower(), string)


def from_string(string):
    m = re.match("^(?:(\d+) )?([-'\w\s]+) (\d+)$", string.strip())
    if not m:
        raise Exception('Invalid date string')

    day = int(m.group(1)) if m.group(1) else 1
    month = m.group(2).lower()
    year = int(m.group(3))

    if month in holiday_months:
        days = 2
    elif month in holidays:
        days = 1
    elif month in months:
        days = 30
    else:
        raise Exception('Invalid month')

    if day > days:
        raise Exception('Invalid day')

    if month == 'overlithe' and not is_leap_year(year):
        raise Exception('Not a leap year')

    return Date(year, month, day)


# Date object

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def to_string(self):
        if self.month in holidays:
            return '{} {}'.format(title_case(self.month), self.year)
        else:
            return '{} {} {}'.format(self.day, title_case(self.month), self.year)

    def to_day_of_year(self):
        if self.month == 'yule':
            return 1 if self.day == 2 else get_days_in_year(self.year)
        elif self.month == 'lithe':
            return 182 if self.day == 1 else (185 if is_leap_year(self.year) else 184)
        elif self.month == 'mid-year\'s day':
            return 183
        elif self.month == 'overlithe':
            return 184
        else:
            month_index = months.index(self.month)
            holiday_count = 1 + (0 if month_index < 6 else (4 if leap_year else 3))
            return (month_index * 30 + holiday_count + self.day)

    def add_days(self, count):
        day_index = self.to_day_of_year() + count
        year = self.year

        while day_index > get_days_in_year(year):
            day_index -= get_days_in_year(year)
            year += 1

        while day_index < 1:
            year -= 1
            day_index += get_days_in_year(year)

        return Date(year, month_from_day_of_year(day_index, year),
                    day_of_month_from_day_of_year(day_index, year))
