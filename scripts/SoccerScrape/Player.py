class Player:

    def __init__(self, rosterYear, firstName,
                lastName, grade, position, height, homeTown,
                state_or_country, highSchool, previousSchool,
                college, collegeLeague):
        self.rosterYear = rosterYear
        self.firstName = firstName
        self.lastName = lastName
        self.grade = grade
        self.position = position
        self.homeTown = homeTown
        self.state_or_country = state_or_country
        self.highSchool = highSchool
        self.previousSchool = previousSchool
        self.college = college
        self.collegeLeague = collegeLeague
        self.height = height

    def append_student_to_csv(self):
        with open('soccer_data.csv', 'a') as f:
            row = [self.rosterYear, self.firstName, self.lastName, self.grade, self.position,
            self.height, self.homeTown, self.state_or_country, self.highSchool, self.previousSchool,
            self.college, self.collegeLeague]

            writer = csv.writer(f, lineterminator = "\n")
            writer.writerow(row)

    def get_roster_grade(self):
        return self.rosterYear

    def get_id(self):
        return self.id

    def get_first_name(self):
        return self.firstName

    def get_last_name(self):
        return self.lastName

    def get_grade(self):
        return self.grade

    def get_position(self):
        return self.position

    def get_home_town(self):
        return self.homeTown

    def get_state_or_country(self):
        return self.state_or_country

    def get_high_school(self):
        return self.highSchool

    def get_previous_school(self):
        return self.previousSchool

    def get_college(self):
        return self.college

    def get_college_league(self):
        return self.collegeLeague

    def get_height(self):
        return self.height

    def get_JSON(self):
        return {
            'id: '              : self.id,
            'rosterYear: '      : self.rosterYear,
            'firstName: '       : self.firstName,
            'lastName: '        : self.lastName,
            'grade: '           : self.grade,
            'position: '        : self.position,
            'height: '          : self.height
            'homeTown: '        : self.homeTown,
            'state_or_country: ': self.state_or_country,
            'highSchool: '      : self.highSchool,
            'previousSchool'    : self.previousSchool
            'college: '         : self.college,
            'collegeLeague: '   : self.collegeLeague
        }

    def __str__(self):
        return ("id: " + str(self.id) + "\nrosterYear: " + self.rosterYear + "\nfirstName: " + self.firstName + "\nlastName: "
         + self.lastName + "\ngrade: " + self.grade + "\nposition: " + self.position
         + "\nheight: " + self.height + "\nhomeTown: " + self.homeTown + "\nState or Country: " + self.state_or_country + "\nhighSchool: " + self.highSchool
         + "\npreviousSchool: " self.previousSchool + "\ncollege: " + self.college + "\ncollegeLeague: " + self.collegeLeague)
