import os, re, csv
from CustomExceptions import YearError, GPGSLogicError
def gather_hyphenated_names():
    """
        Method searches for the hyphenated last names in the statistics files in ../starter_data dir
    """
    files = os.listdir('../starter_data')
    for file in files:
        if '.txt' in file:
            stat_year = file[re.search('\d', file).start():file.index('.txt')] #extract year out of the file name
            with open(file, 'r') as f:
                head = [next(f) for x in range(3)]
                data = f.readlines()
                year   = head[1].strip()

                if year != stat_year:
                    raise YearError('The year in file ' + file + ' conflicts with filename')

                line_count = 0
                for line in data:
                    if line is not '\n':
                        line_count += 1
                        line = line.strip() #stripping newline char from line
                        split_line = line.split(' ')
                        try:
                            lastName  = split_line[2]
                        except:
                            print('\n\n\nException with splitting the line! Check for extra newline characters.\
                                  Line is: ', line, line_count)
                            print('File is: ', file)

                        if '-' in lastName:
                           print(file, year, lastName, line_count)

def append_stored_starter_data():
    """
        Method appends the statistics in ../starter_data .txt files to starter_data.csv
    """
    files = os.listdir('../starter_data')
    for file in files:
        if '.txt' in file:
            stat_year = file[re.search('\d', file).start():file.index('.txt')] #extract year out of the file name
            with open('../starter_data/' + file, 'r') as f:
                head = [next(f) for x in range(3)]
                data = f.readlines()
                school = head[0].strip()
                year   = head[1].strip()
                potential_starts = head[2].split(':')[1].strip()

                if year != stat_year:
                    raise YearError('The year in file ' + file + ' conflicts with filename')

                for line in data:
                    if line is not '\n':
                        number = firstName = lastName = gs = gp = None
                        line = line.strip()
                        split_line = line.split(' ')
                        if re.search('\d', split_line[0]) is not None: #number is first thing
                            number = split_line[0]
                        else:
                            number = 'NA'

                        if len(split_line) == 4: # no. fn ln gp-gs
                            firstName = split_line[1].strip()
                            if ',' in firstName:
                                firstName = ' '.join(firstName.split(',')).strip()

                            lastName = split_line[2].strip()
                            if ',' in lastName:
                                lastName = ' '.join(lastName.split(',')).strip()
                            try:
                                gp = split_line[3].split('-')[0].strip()
                                gs = split_line[3].split('-')[1].strip()
                            except Exception as e:
                                print('Error acquiring gp/gs in file', file, 'line:', line)
                                print(e)

                        elif len(split_line) == 3 and number is not 'NA': #no last name case
                            firstName = split_line[1].strip()
                            lastName = 'NA'
                            if ',' in firstName:
                                firstName = ' '.join(firstName.split(',')).strip()
                            try:
                                gp = split_line[2].split('-')[0].strip()
                                gs = split_line[2].split('-')[1].strip()
                            except Exception as e:
                                print('Error acquiring gp/gs in file', file, 'line:', line)
                                print(e)
                        else:
                            print('Line reached that was less than 3 in length and first entry not a number. '  \
                                  'See to file: ', file, 'line:', line)

                        if int(gp) > int(potential_starts):
                            raise GPGSLogicError('Error: GP > Potential Starts in ' + file)

                        is_starter = determine_is_starter(gs, potential_starts)

                        with open('starter_data.csv', 'a', newline= '\n') as f:
                            row = [year, number, firstName, lastName, potential_starts, gp, gs, is_starter, school]
                            writer = csv.writer(f, lineterminator = "\n")
                            writer.writerow(row)


def determine_is_starter(gs, potential_starts):
    """
        Method determines if gs/potential_starts is .5 or not to determine if player is a starter
    """
    if int(gs)/int(potential_starts) >= .5:
        return 'Y'
    return 'N'
