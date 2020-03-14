class Starter():

    def __init__(self, year, number, firstName, lastName,
                 potential_starts, gp, gs, is_starter, college):

        self.roster_year = year
        self.number = number
        self.firstName = firstName
        self.lastName = lastName
        self.potential_starts = potential_starts
        self.gp = gp
        self.gs = gs
        self.is_starter = is_starter
        self.college = college


    def __eq__(self, other):
        return self.roster_year == other.roster_year \
               and self.number == other.number \
               and self.lastName == other.lastName \
               and self.college == other.college

    def __str__(self):
        return 'roster_year: ' + self.roster_year + '\n' + 'number: ' + self.number + '\n' + 'lastName: ' \
                + self.lastName + '\n' + 'college: ' + self.college



