#%%
import sys, csv, re, unidecode
from CustomExceptions import YearError, GPGSLogicError
sys.path.append('..')
sys.path.append('../spiders')
import CurrentRosterYear
from soccerspider import SoccerSpider
from TableSpider import TableSpider
from TableSpiderDuke import TableSpiderDuke
from TableSpiderHarvard import TableSpiderHarvard
from TableSpiderWM import TableSpiderWM
from GPGSAmerican import GPGSAmericanUniversity
from GPGSCornell import GPGSCornell
from GPGSFurman import GPGSFurman
from GPGSHolyCross import GPGSHolyCross
from GPGSListView import GPGSSpider
from NewRosterDataListViewSpider import NewRosterDataListSpider
from NewRosterDataTableSpiderWM import NewRosterDataTableWMSpider
from NewRosterDataTableViewDukeSpider import NewRosterDataTableDukeSpider
from NewRosterDataTableViewHarvard import NewRosterDataTableHarvardSpider
from NewRosterDataTableViewSpider import NewRosterDataTableSpider
from append import determine_is_starter
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from Starter import Starter


class DataCollector():
    """
        Class that has methods to collect the data for the project. Only should call append_new_starter_data
        and append_new_roster_data to add data to the csv files
    """

    def __init__(self):
        pass

    def collect_new_roster_data(self):
        """
            Method collects roster data for current roster year
        """
        configure_logging() #uncomment for debug log
        runner = CrawlerRunner(get_project_settings())

        @defer.inlineCallbacks
        def _crawl():
            yield runner.crawl(NewRosterDataListSpider)
            yield runner.crawl(NewRosterDataTableSpider)
            yield runner.crawl(NewRosterDataTableDukeSpider)
            yield runner.crawl(NewRosterDataTableHarvardSpider)
            yield runner.crawl(NewRosterDataTableWMSpider)
            reactor.stop()

        _crawl()

        try:
            reactor.run() # the script will block here until all crawling jobs are finished
        except:
            pass

    def collect_new_and_prior_roster_data(self):

        """
            Method collects roster data from 2006 onward
        """

        with open('roster_data.csv', 'w') as f: #writing header
            fieldNames = ['Roster_Year', 'Player_Number', 'First_Name', 'Last_Name', 'Year',
            'Position', 'Height', 'Weight', 'Home_Town', 'State_or_Country', 'High_School',
            'Previous_School', 'College', 'College_League', 'Bio_Link']
            fileWriter = csv.DictWriter(f, fieldnames = fieldNames, lineterminator = "\n")
            fileWriter.writeheader()

        configure_logging() #uncomment for debug log

        runner = CrawlerRunner(get_project_settings())


        @defer.inlineCallbacks
        def _crawl():
            yield runner.crawl(SoccerSpider)
            yield runner.crawl(TableSpider)
            yield runner.crawl(TableSpiderDuke)
            yield runner.crawl(TableSpiderHarvard)
            yield runner.crawl(TableSpiderWM)
            reactor.stop()

        _crawl()

        try:
            reactor.run() # the script will block here until all crawling jobs are finished
        except:
            pass

    @classmethod
    def append_incoming_roster_data(self):
        self.collect_new_roster_data()
        new_data = []
        with open('incoming_roster_data.csv', 'r') as f:
            for line in f:
               data = line.split(',')
               data[-1] = data[-1].strip() #stripping newline char
               new_data.append(data)

        with open('roster_data.csv', 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            for data in new_data:
                writer.writerow(data)



    #%%
    def eliminate_duplicates_starter_data_set(self, fileName):
        """
        removes duplicate starters in stater data set who have lower amount games started than their duplicate
        """
        players = []
        with open(fileName, 'r') as f:
            for line in f:
                data = line.strip().split(',')
                try:
                    starter = Starter(data[0], data[1], data[2],
                                      data[3], data[4], data[5],
                                      data[6], data[7], data[8])
                except:
                    return
                if starter in players:
                    seen_starter_index = players.index(starter)
                    seen_starter = players[seen_starter_index]
                    if starter.gs > seen_starter.gs:
                        players.remove(seen_starter)
                        players.append(starter)
                        print('Removed Duplicate Starter: ', starter)
                else:
                    players.append(starter)

        with open(fileName, 'w') as f:
            writer = csv.writer(f, lineterminator = '\n')
            for player in players:
                writer.writerow([player.roster_year, player.number,
                                 player.firstName, player.lastName,
                                 player.potential_starts, player.gp,
                                 player.gs, player.is_starter,
                                 player.college])


    @classmethod
    def __collect_duke_starter_data(self):
        """
            Appends duke's current roster year data to starter_data.txt. Make sure duke's file is named
            'Duke****'.txt where **** is the current roster year
        """
        roster_year = CurrentRosterYear.get_current_roster_year().split('-')[0]
        fileName = '../starter_data/Duke' + roster_year + '.txt'
        with open(fileName, 'r') as f:
            stat_year = fileName[re.search('\d', fileName).start():fileName.index('.txt')] #extract year out of the file name
            head = [next(f) for x in range(3)]
            data = f.readlines()
            school = head[0].strip()
            year   = head[1].strip()
            potential_starts = head[2].split(':')[1].strip()

            if year != stat_year:
                raise YearError('The year in file ' + f + ' conflicts with filename')

            for line in data:
                if line != '\n':
                    number = firstName = lastName = gs = gp = None
                    line = line.strip()
                    split_line = line.split(' ')
                    if re.search('\d', split_line[0]) is not None: #number is first element
                        number = split_line[0]
                    else:
                        number = 'NA'

                    if len(split_line) == 4: # number fn ln gp-gs
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
                                print('Error acquiring gp/gs in file', f, 'line:', line)
                                print(e)

                    elif len(split_line) == 3 and number != 'NA': #no last name case
                        firstName = split_line[1].strip()
                        lastName = 'NA'
                        if ',' in firstName:
                            firstName = ' '.join(firstName.split(',')).strip()
                        try:
                            gp = split_line[2].split('-')[0].strip()
                            gs = split_line[2].split('-')[1].strip()
                        except Exception as e:
                            print('Error acquiring gp/gs in file', f, 'line:', line)
                            print(e)
                    else:
                        print('Line reached that was less than 3 in length and first entry not a number. '  \
                                  'See to file and handle case: ', f, 'line:', line)

                    if int(gp) > int(potential_starts):
                        raise GPGSLogicError('Error: GP > Potential Starts in ' + f)

                    is_starter = determine_is_starter(gs, potential_starts)

                    with open('incoming_starter_data.csv', 'a', newline= '\n') as f:
                        row = [year, number, firstName, lastName, potential_starts, gp, gs, is_starter, school]
                        writer = csv.writer(f, lineterminator = "\n")
                        writer.writerow(row)


    def collect_new_starter_data(self): #may need to reset the kernel. Remember Duke University needs it's own entry
        """
           method collects incoming starter data for current roster year
        """
        configure_logging()
        runner = CrawlerRunner(get_project_settings())

        self.__collect_duke_starter_data()

        @defer.inlineCallbacks
        def _crawl():
            yield runner.crawl(GPGSAmericanUniversity)
            yield runner.crawl(GPGSCornell)
            yield runner.crawl(GPGSFurman)
            yield runner.crawl(GPGSHolyCross)
            yield runner.crawl(GPGSSpider)
            reactor.stop()

        _crawl()

        try:
            reactor.run()
        except:
            pass

        self.eliminate_duplicates_starter_data_set('incoming_starter_data.csv')


    def append_new_starter_data(self):
        """
         appends the incoming starter data for this roster year to starter_data.csv
        """
        self.collect_new_starter_data()
        new_data = []
        with open('incoming_starter_data.csv', 'r') as f:
            for line in f:
               data = line.split(',')
               data[-1] = data[-1].strip() #stripping newline char
               new_data.append(data)

        with open('starter_data.csv', 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            for data in new_data:
                writer.writerow(data)


#%%
    def has_date(self, word):
        return re.search('[0-3][0-9]{3}', word) is not None

    def extract_prior_conference_data(self, debug):
        """
        Calls all the extract conference methods to form one data set in accolades.csv
        @param debug: boolean for debugging messages
        """
        if debug: print('-'* 20, 'LOADING PATRIOT LEAGUE CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_patriot_league_conference_data(debug)
        if debug: print('-'* 20, 'LOADING IVY LEAGUE CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_ivy_league_conference_data(debug)
        if debug: print('-'* 20, 'LOADING CAA CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_caa_conference_data(debug)
        if debug: print('-'* 20, 'LOADING SOUTHERN LEAGUE CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_southern_conference_data(debug)
        if debug: print('-'* 20, 'LOADING ACC CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_acc_conference_data(debug)
        if debug: print('-'* 20, 'LOADING AMERICAN ATHLETIC CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_americanathletic_conference_data(debug)
        if debug: print('-'* 20, 'LOADING A10 CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_a10_conference_data(debug)
        if debug: print('-'* 20, 'LOADING BIG10 CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_big10_conference_data(debug)
        if debug: print('-'* 20, 'LOADING STANFORD CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_stanford_conference_data(debug)
        if debug: print('-'* 20, 'LOADING WAC CONFERENCE DATA', '-'*20, '\n')
        self.extract_prior_wac_conference_data(debug)

    def extract_prior_patriot_league_conference_data(self, debug):
        """
        extracts data out of the patriot league conference
        txt file in conference_data folder
        Type debug: bool for debugging output
        """
        with open('../conference_data/Patriot.txt') as f:
           year = accolade = first_name = last_name = college = None
           for line in f:
               if self.has_date(line):
                   year = line.strip()
               else:
                   players = line.split(';')
                   for player in players:
                       college_index = self.__get_patriot_or_ivy_college_index(player)
                       college = ' '.join(player.split()[college_index:])
                       college = re.sub('[()]+', '', college)
                       college = self.__convert_to_full_college_name(college)
                       if 'Team' in player:
                           accolade   = player.split()[0].strip()
                           accolade   = re.sub('-', ' ', accolade)
                           first_name = player.split()[3].strip()
                           last_name  = ' '.join(player.split()[4:college_index]).strip()
                       else:
                           first_name = player.split()[0].strip()
                           last_name  = ' '.join(player.split()[1:college_index]).strip()

                       if debug:
                           self.__print_conference_data_debug_message([player],
                                                                      [year, first_name, last_name, accolade, college])

                       self.__append_conference_datum(year, first_name, last_name, accolade, college)

    def extract_prior_ivy_league_conference_data(self, debug):
        """
         extracts data out of the ivy league conference txt file in conference_data folder
         Type debug: bool for debugging output
        """
        with open('../conference_data/Ivy.txt') as f:
           year = accolade = first_name = last_name = college = None
           for line in f:
               if self.has_date(line):
                   year = line.strip()
               else:
                   cleaned_line = re.sub('[A-Z]{1,2}?, ', '', line)
                   cleaned_line = re.sub('\n', '', cleaned_line)
                   players = cleaned_line.split(',')
                   for player in players:
                       college_index = self.__get_patriot_or_ivy_college_index(player)
                       college = ' '.join(player.split()[college_index:]).strip()
                       college = re.sub('[()]+', '', college)
                       college = self.__convert_to_full_college_name(college)
                       if 'Team' in player or 'Mention' in player:
                           accolade   = ' '.join(player.split()[0:2]).strip()
                           first_name = player.split()[3].strip()
                           last_name  = ' '.join(player.split()[4:college_index]).strip()
                       else:
                           first_name = player.split()[0].strip()
                           last_name  = ' '.join(player.split()[1:college_index]).strip()

                       if debug:
                           self.__print_conference_data_debug_message([player],
                                                                      [year, first_name, last_name, accolade, college])

                       self.__append_conference_datum(year, first_name, last_name, accolade, college)

    def extract_prior_caa_conference_data(self, debug):
        """
        extracts prior CAA conference data and sends to accolades.csv
        @param debug whether to print debug messages (bool)
        """
        with open('../conference_data/CAA.txt') as f:
           year = accolade = first_name = last_name = college = None
           for line in f:
               if self.has_date(line):
                   year = line.strip()
               else:
                   players = line.split(';')
                   for player in players:
                       college = player.split(',')[-1].strip()
                       college = self.__convert_to_full_college_name(college)
                       if 'Team' in player:
                           accolade   = player.split(':')[0]
                           first_name = player.split(':')[1].split(',')[0].split()[0].strip()
                           last_name  = ' '.join(player.split(':')[1].split(',')[0].split()[1:]).strip()
                       else:
                           first_name = player.split(',')[0].split()[0].strip()
                           last_name  = ' '.join(player.split(',')[0].split()[1:]).strip()
                       if debug:
                           self.__print_conference_data_debug_message([player],
                                                                      [year, first_name, last_name, accolade, college])

                       self.__append_conference_datum(year, first_name, last_name, accolade, college)


    def extract_prior_acc_conference_data(self, debug):
        """
        Method processes acc conference data.
        @param debug: boolean whether to print debugging messages
        Note: ACC pdf format so poor, had to copy and paste data to text file
        """
        year = accolade = first_name = last_name = college = None
        with open('../conference_data/ACC.txt', 'r') as f:
            for line in f:
                if self.has_date(line):
                    year = line.strip()
                elif 'Team' in line:
                    accolade = line.strip()
                else:
                    cleaned_line = re.sub('\\.{2,}', ' ', line).strip()
                    print(cleaned_line)
                    first_name   = cleaned_line.split()[1].strip()
                    last_name    = ' '.join(cleaned_line.split()[2:-1]).strip()
                    college      = cleaned_line.split()[-1].strip()
                    college = self.__convert_to_full_college_name(college)

                    if debug:
                        self.__print_conference_data_debug_message([year, first_name, last_name, accolade, college],
                                                               [year, first_name, last_name, accolade, college])
                    self.__append_conference_datum(year, first_name, last_name, accolade, college)

    def extract_prior_a10_conference_data(self, debug):
        """
        Method processes A10 conference data.
        @param debug: boolean whether to print debugging messages
        Note: A10 pdf format so poor, had to copy and paste data to text file
        """
        year = accolade = first_name = last_name = college = None
        with open('../conference_data/A10.txt', 'r') as f:
            for line in f:
                if self.has_date(line):
                    year = line.strip()
                elif 'Team' in line or 'Mention' in line:
                    accolade = line.strip()
                else:
                   cleaned_line = re.sub(',', '', line).strip()
                   players = cleaned_line.split(';')
                   for player in players:
                       player = re.sub('[A-Z]{1}[(]', 'X (', player) #creating uniformity in the data
                       if len(player.split()) == 3:
                           player = re.sub(' [(]', ' X (', player) #creating uniformity in the data
                       split_player = player.split()
                       first_name = split_player[0].strip()
                       last_name  = ' '.join(split_player[1:-2]).strip()
                       college = re.sub('[()]+', '', split_player[-1]).strip()
                       college = self.__convert_to_full_college_name(college)
                       if debug:
                           self.__print_conference_data_debug_message([year, first_name, last_name, accolade, college],
                                                               [year, first_name, last_name, accolade, college])
                       self.__append_conference_datum(year, first_name, last_name, accolade, college)

    def extract_prior_southern_conference_data(self, debug):
        year = accolade = first_name = last_name = college = None
        with open('../conference_data/Southern.txt', 'r') as f:
            for line in f:
                if self.has_date(line):
                    year = line.strip()
                elif 'Team' in line or 'Mention' in line:
                    accolade = line.strip()
                else:
                   cleaned_line = re.sub(' +', ' ', line)
                   split_line = cleaned_line.split(',')
                   first_name = split_line[0].split()[1].strip()
                   last_name  = ' '.join(split_line[0].split()[2:]).strip()
                   college    = split_line[1].strip()
                   college    = self.__convert_to_full_college_name(college)
                   if debug:
                       self.__print_conference_data_debug_message([year, first_name, last_name, accolade, college],
                                                               [year, first_name, last_name, accolade, college])
                   self.__append_conference_datum(year, first_name, last_name, accolade, college)

    def extract_prior_americanathletic_conference_data(self, debug):
        year = accolade = first_name = last_name = college = None
        with open('../conference_data/AmericanAthletic.txt', 'r') as f:
            for line in f:
                if self.has_date(line):
                    year = line.strip()
                elif 'Team' in line or 'Mention' in line:
                    accolade = line.strip()
                else:
                   cleaned_line = re.sub(' +', ' ', line)
                   split_line = cleaned_line.split(',')
                   first_name = split_line[0].split()[0].strip()
                   last_name  = ' '.join(split_line[0].split()[1:]).strip()
                   college    = split_line[-1]
                   college    = re.sub('\\*', '', college).strip()
                   college    = self.__convert_to_full_college_name(college)
                   if debug:
                       self.__print_conference_data_debug_message([year, first_name, last_name, accolade, college],
                                                               [year, first_name, last_name, accolade, college])
                   self.__append_conference_datum(year, first_name, last_name, accolade, college)

    def extract_prior_big10_conference_data(self, debug):
        """
        Extracts big10 conference data fromt txt file. Appends to accolades.csv
        @param debug boolean: set True for debugging messages
        """
        year = accolade = first_name = last_name = college = None
        with open('../conference_data/Big10.txt', 'r') as f:
            for line in f:
                line = re.sub('\n', '', line)
                if 'Team' in line:
                    accolade = line.strip()
                elif len(line.split()) == 1 or len(line.split()) == 2:
                    college = self.__convert_to_full_college_name(line)
                else:
                    first_name = line.split(',')[0].split()[0].strip()
                    last_name  = ' '.join(line.split(',')[0].split()[1:]).strip()
                    years      = line.split(',')[-1].strip()
                    for year in years.split('-'):
                        if len(year) == 2:
                            year = '20' + year

                        if debug:
                            self.__print_conference_data_debug_message([year, first_name, last_name, accolade, college],
                                                               [year, first_name, last_name, accolade, college])

                        self.__append_conference_datum(year, first_name, last_name, accolade, college)

    def extract_prior_stanford_conference_data(self, debug):
        """
        Extracts conference data for Stanford University from Stanford.txt
        @param debug boolean: set True for debugging messages
        """
        with open('../conference_data/Stanford.txt', 'r') as f:
            for line in f:
                college = 'Stanford University'
                year    = line.split()[0].strip()
                first_name = line.split()[1].strip()
                last_name  = line.split()[2].strip()
                accolade   = ' '.join(line.split()[-2:]).strip()
                if debug:
                    self.__print_conference_data_debug_message([year, first_name, last_name, accolade, college],
                                                               [year, first_name, last_name, accolade, college])

                self.__append_conference_datum(year, first_name, last_name, accolade, college)

    def extract_prior_wac_conference_data(self, debug):
        """
        Extracts conference data for WAC conference from WAC.txt
        @param debug boolean: set True for debugging messages
        """
        with open ('../conference_data/WAC.txt', 'r') as f:
            year = college = first_name = last_name = accolade = None
            for line in f:
                if self.has_date(line):
                    year = line.split()[0].strip()
                elif 'Team' in line:
                    accolade = line.strip()
                else:
                    data = line.strip().split(',')
                    name = data[0].strip().split()
                    first_name = name[0].strip()
                    last_name = ' '.join(name[1:]).strip()
                    college = data[-1].strip()
                    college = self.__convert_to_full_college_name(college)
                    if debug:
                        self.__print_conference_data_debug_message([year, first_name, last_name, accolade, college],
                                                               [year, first_name, last_name, accolade, college])

                    self.__append_conference_datum(year, first_name, last_name, accolade, college)

    @classmethod
    def __get_patriot_or_ivy_college_index(self, player):
        """
        Gets the index where the college name occurs in a chunk of patriot league conference data
        @param player a string representing a player
        """
        index = 0
        for chunk in player.split():
            if '(' in chunk:
                break
            index += 1
        return index

    @classmethod
    def __convert_to_full_college_name(self, college):
        """
        converting a college's shortened name to full
        """
        if '.' in college:
            college = college[0:college.index('.')]
        index = {

                'Lehigh'         : 'Lehigh University',
                'Holy Cross'     : 'College of the Holy Cross',
                'Bucknell'       : 'Bucknell University',
                'Loyola Maryland': 'Loyola University Maryland',
                'Loyola'         : 'Loyola University Maryland',
                'Boston U'      : 'Boston University',
                'Boston University': 'Boston University',
                'Lafayette'      : 'Lafayette College',
                'Colgate'        : 'Colgate University',
                'Army'           : 'Army West Point',
                'Army West Point': 'Army West Point',
                'Air Force'      : 'Air Force Academy',
                'American'       : 'American University',
                'Navy'           : 'Naval Academy',
                'Yale'           : 'Yale University',
                'Harvard'        : 'Harvard University',
                'Penn'           : 'University of Pennsylvania',
                'Princeton'      : 'Princeton University',
                'Columbia'       : 'Columbia University',
                'Cornell'        : 'Cornell University',
                'Brown'          : 'Brown University',
                'Dartmouth'      : 'Dartmouth College',
                'NU'             : 'Northeastern University',
                'Northeastern'   : 'Northeastern University',
                'W&M'            : 'College of William & Mary',
                'DU'             : 'Duke University',
                'BC'             : 'Boston College',
                'WF'             : 'Wake Forest University',
                'ND'             : 'University of Notre Dame',
                'SU'             : 'Syracuse University',
                'DAV'            : 'Davidson College',
                'Furman'         : 'Furman University',
                'Wofford'        : 'Wofford College',
                'Woff ord'       : 'Wofford College',
                'SMU'            : 'Southern Methodist University',
                'Northwestern'   : 'Northwestern University'

                }

        return index.get(college, college + ' NOT APPLICABLE')

    @classmethod
    def __print_conference_data_debug_message(self, data, attributes):
        """
        prints a debug message for the all-conference data collection
        given a list of attributes

        type attributes: list of strings
        type data: The data the attributes were aquired from
        """
        print('-'*20 + 'Extracted Player Data Based On Split' + '-'*20)
        print(data)
        print('-'*20 + 'What Will Go to CSV File (Decoded)' + '-'*20)
        print(attributes)

    @classmethod
    def __append_conference_datum(self, year, first_name, last_name,
                                  accolade, college):
        """
        appends parsed attributes to all-conference data to 'accolades.csv'
        input to function are the parsed parameters
        """

        with open('accolades.csv', 'a', newline = '\n') as f:
            writer = csv.writer(f, lineterminator = '\n')
            row = [year, unidecode.unidecode(first_name), unidecode.unidecode(last_name),
                   accolade, unidecode.unidecode(college)]
            writer.writerow(row)
