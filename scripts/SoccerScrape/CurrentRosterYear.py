import datetime

def get_current_roster_year():
    """
        get_current_roster_year() returns a string of the current roster year such as 2018-19
        rtype: string
    """
    current_year  = int(datetime.date.today().strftime("%Y"))
    year_two_ints = int(datetime.date.today().strftime("%y"))
    current_month = int(datetime.date.today().strftime("%M"))
    if current_month < 8: #calendar year ahead of starting roster year
        current_year -= 1
    if current_month >= 8: #calendar year behind ending roster year
        year_two_ints += 1
    return str(current_year) + '-' + str(year_two_ints)