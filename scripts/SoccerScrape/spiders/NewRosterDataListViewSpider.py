import scrapy
import re
import sys
sys.path.append('..')
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from items import Player
from LeagueDictionary import get_college_from_url, check_league

class NewRosterDataListSpider(scrapy.Spider):

    """
        A spider that parses various schools' men's soccer rosters that have websites like Lafayette's
        Only for current roster year
    """
    name = "newRosterDataListSpider"

    custom_settings = {
                'ITEM_PIPELINES':{
                        'SoccerScrape.pipelines.IncomingPlayerPipeline': 300,
                        }
            }

    start_urls = [
        'https://www.goleopards.com/roster.aspx?path=msoc',
        'https://lehighsports.com/roster.aspx?path=msoc',
        'https://gocolgateraiders.com/roster.aspx?path=msoc',
        'https://goprincetontigers.com/roster.aspx?path=msoc',
        'https://goterriers.com/roster.aspx?path=msoc',
        'https://bucknellbison.com/roster.aspx?path=msoc',
        'https://loyolagreyhounds.com/roster.aspx?path=msoc',
        'https://navysports.com/roster.aspx?path=msoc',
        'https://pennathletics.com/roster.aspx?path=msoc',
        'https://brownbears.com/roster.aspx?path=msoc',
        'https://dartmouthsports.com/roster.aspx?path=msoc',
        'https://gocolumbialions.com/roster.aspx?path=msoc',
        'https://gostanford.com/roster.aspx?path=msoc',
        'https://und.com/roster.aspx?path=msoc',
        'http://georgetown.sidearmsports.com/roster.aspx?path=msoc',
        'https://godeacs.com/roster.aspx?path=msoc',
        'https://bceagles.com/roster.aspx?path=msoc',
        'https://villanova.com/roster.aspx?path=msoc',
        'https://cuse.com/roster.aspx?path=msoccer',
        'https://smumustangs.com/roster.aspx?path=msoc',
        'https://davidsonwildcats.com/roster.aspx?path=msoc',
        'https://goairforcefalcons.com/roster.aspx?path=msoc',
        'https://woffordterriers.com/roster.aspx?path=msoc',
        'https://nuhuskies.com/roster.aspx?path=msoc'
    ]

    allowed_domains = [
        'www.goleopards.com',
        'lehighsports.com',
        'gocolgateraiders.com',
        'goprincetontigers.com',
        'goterriers.com',
        'bucknellbison.com',
        'loyolagreyhounds.com',
        'navysports.com',
        'pennathletics.com',
        'brownbears.com',
        'dartmouthsports.com',
        'gocolumbialions.com',
        'gostanford.com',
        'und.com',
        'georgetown.sidearmsports.com',
        'godeacs.com',
        'bceagles.com',
        'villanova.com',
        'cuse.com',
        'smumustangs.com',
        'davidsonwildcats.com',
        'goairforcefalcons.com',
        'woffordterriers.com',
        'nuhuskies.com'
    ]

    #xpath strings for a common type of format that multiple websites share
    PLAYER_LIST_VIEW =  '//li[@class="sidearm-roster-player"]'

    NAME_FROM_LIST_VIEW = './/div[@class = "sidearm-roster-player-name"]/p/a/text()' #player names, first and last

    PROFILE_LINK_FROM_LIST_VIEW = './/div[@class = "sidearm-roster-player-name"]/p/a/@href' #profile bio

    ROSTER_YEAR_FROM_LIST_VIEW = './/article[@class = "sidearm-roster-view sidearm-common"]/h2/text()' #year of roster

    POSITION_LIST_VIEW = './/div[@class = "sidearm-roster-player-position"]/span[@class="text-bold"]/text()' #player positions

    ALTERNATIVE_POSITION_LIST_VIEW = ('.//div[@class = "sidearm-roster-player-position"]/span[@class="text-bold"]' +
                                    '/span[@class = "sidearm-roster-player-position-long-short hide-on-medium"]/text()') #in case POSITION_LIST_VIEW returns None

    HEIGHT_LIST_VIEW = './/span[@class = "sidearm-roster-player-height"]/text()'

    ACADEMIC_YEAR_LIST_VIEW = ('.//div[@class = "sidearm-roster-player-class-hometown"]/' +
                                'span[@class = "sidearm-roster-player-academic-year"]/text()') #e.g Freshman

    HOME_TOWN_LIST_VIEW = ('.//div[@class = "sidearm-roster-player-other hide-on-large"]/'
                           + 'div[@class = "sidearm-roster-player-class-hometown"]' +
                            '/span[@class = "sidearm-roster-player-hometown"]/text()')
    #e.g Surrey, England or New York, N.Y.

    HIGH_SCHOOL_LIST_VIEW = ('.//div[@class = "sidearm-roster-player-other flex-item-1 columns hide-on-medium-down"]' + #list of high schols
                        '/div[@class = "sidearm-roster-player-class-hometown"]' +
                        '/span[@class = "sidearm-roster-player-highschool"]/text()')

    PREVIOUS_SCHOOL_LIST_VIEW = ('.//div[@class = "sidearm-roster-player-other flex-item-1 columns hide-on-medium-down"]' + #list of previous schools
                        '/div[@class = "sidearm-roster-player-class-hometown"]' +
                        '/span[@class = "sidearm-roster-player-previous-school"]/text()')

    NUMBER_LIST_VIEW ='.//div[@class = "sidearm-roster-player-name"]/span/span[@class = "sidearm-roster-player-jersey-number"]/text()'

    WEIGHT_LIST_VIEW = './/span[@class = "sidearm-roster-player-weight"]/text()'


    def start_requests(self):
        """
            Starts the http request
        """
        for u in self.start_urls:
            try:
                yield scrapy.Request(u, callback=self.parse_list,
                errback=self.errback_httpbin, dont_filter=True)
            except ValueError:
                print("ValueError")
                continue


    def parse_list(self, response):

        self.logger.debug('Got successful response from {}'.format(response.url))

        players    = response.xpath(NewRosterDataListSpider.PLAYER_LIST_VIEW) #list of <li/> nodes for each player
        rosterYear = response.xpath(NewRosterDataListSpider.ROSTER_YEAR_FROM_LIST_VIEW).extract_first().split(" ") #format is a list of strings containing roster year e.g

        for word in rosterYear: #the rosterYear could be within a string
            if word.isnumeric() or '-' in word:
                rosterYear = word
                break


        REGREX = "[^-A-Za-z/&'.,Íö0-9`()~\s]+"

        for player in players: #time to parse

            name                = player.xpath(NewRosterDataListSpider.NAME_FROM_LIST_VIEW).extract_first() #string with a single name e.g 'John Doe'
            position            = player.xpath(NewRosterDataListSpider.POSITION_LIST_VIEW).extract_first() #string with a single position, unstriped e.g "\tGK\t"
            alternativePosition = player.xpath(NewRosterDataListSpider.ALTERNATIVE_POSITION_LIST_VIEW).extract_first() #if position was an empty string, this will be the position
            classYear           = player.xpath(NewRosterDataListSpider.ACADEMIC_YEAR_LIST_VIEW).extract_first() #string of a class year e.g 'Freshman'
            home                = player.xpath(NewRosterDataListSpider.HOME_TOWN_LIST_VIEW).extract_first() #string of a single hometown e.g 'Easton, PA'
            highSchool          = player.xpath(NewRosterDataListSpider.HIGH_SCHOOL_LIST_VIEW).extract_first() #string of single high school e.g 'Tennent'
            previousSchool      = player.xpath(NewRosterDataListSpider.PREVIOUS_SCHOOL_LIST_VIEW).extract_first() #like highSchool
            height              = player.xpath(NewRosterDataListSpider.HEIGHT_LIST_VIEW).extract_first() #string with a single height element e.g ''5'10"'
            number              = player.xpath(NewRosterDataListSpider.NUMBER_LIST_VIEW).extract_first()
            weight              = player.xpath(NewRosterDataListSpider.WEIGHT_LIST_VIEW).extract_first()

            if weight is not None:
                weight = weight[0:weight.lower().index('lbs')].strip()

            playerItem = Player() #creating player item

            self.__process_name(playerItem, name)

            if alternativePosition is not None:
                self.process_other_attribute(playerItem, alternativePosition, 'position')
            else:
                self.process_other_attribute(playerItem, position, 'position')

            self.process_other_attribute(playerItem, classYear, 'classYear')
            self.process_other_attribute(playerItem, height, 'height')
            self.process_other_attribute(playerItem, number, 'number')
            self.process_other_attribute(playerItem, weight, 'weight')

            locationInfo = None
            if(home is not None):
                locationInfo =  home.split(",") #splitting up town and state/country, format is now e.g [Easton Pennsylvania]
            self.__process_location_info(playerItem, locationInfo)


            #Think about refactoring this code--don't like the hardcoded 8
            playerItem['college'] = get_college_from_url(response.url[response.url.index('/')+2:response.url.index('.com')+4]) #cross referencing domain to the school
            playerItem['rosterYear'] = rosterYear




            playerItem['collegeLeague'] = check_league(response.url[response.url.index('/')+2:response.url.index('.com')+4]) #looks up what league the school is in based on url domain

            if highSchool is not None:
                playerItem['highSchool'] = " ".join(re.sub(REGREX, "", highSchool).split()) #keeping only specified values in REGREX for the school
                                                                                                          #eliminating duplicate spaces
                                                                                                          #taking info that is not in ()                                                                                           #that is because club teams are given usually in ()
            else:
                playerItem['highSchool'] = 'NA'

            if previousSchool is not None:
                playerItem['previousSchool'] = " ".join(re.sub(REGREX, "", previousSchool).split())
            else:
                playerItem['previousSchool'] = 'NA'

            href                   = player.xpath(NewRosterDataListSpider.PROFILE_LINK_FROM_LIST_VIEW).extract_first()
            link                   = response.url[0:response.url.index('.com')+4] + href

            playerItem['profileLink'] = link

            yield playerItem


    @classmethod
    def __process_location_info(self, player, locationInfo):
        """
            Processes a player's home town information
            The passed location info is at average case in the format ['city, state_or_country']
        """
        if(locationInfo is None):
            player['homeTown'] = 'NA'
            player['state_or_country'] = 'NA'
            return
        else:
            player['homeTown'] = " ".join(locationInfo[0].split())

        if(len(locationInfo) < 2): #no state/country
            if(locationInfo[0].upper() == 'HONG KONG'): #common case
                player['state_or_country'] = 'China'
            else:
                player['state_or_country'] = 'NA'
        else:
            player['state_or_country']  = " ".join(locationInfo[1].split())

    @classmethod
    def __process_name(self, player, name):
        """
            processes a name for player
            The name format is at average case 'firstName lastName'
        """
        if(name is None): #no name
            player['firstName'] = 'NA'
            player['lastName'] = 'NA'
        elif(len(name.split(" "))==1): #just first name
            player['firstName'] = name.split(' ')[0].strip()
            player['lastName'] = 'NA'
        elif(len(name.split(" ")) == 2): # first and last name
            player['firstName'] = name.split(' ')[0].strip()
            player['lastName'] = name.split(' ')[1].strip()
        else: #name is longer than 2 words
            player['firstName'] = name.split(' ')[0].strip()
            player['lastName'] = " ".join(name.split(' ')[1:]).strip()

    @classmethod
    def process_other_attribute(self, player, attribute, attributeName):
        """
            Processes a generic attribute for player, other than home town information, name, or college
            The attribute parameter is at average case in format 'attributeValue'
        """
        if(attribute is None or attribute.isspace() or \
           (attribute.split("'")[0] == '0' and attributeName is 'height') \
           or attribute == '' or attribute == '-'):

            player[attributeName] = 'NA'
            return
        else:
            if(attributeName == 'height'):
                player[attributeName] = re.sub('"', "", attribute).strip()
                return

        player[attributeName] = re.sub(' +', ' ', attribute.strip())

    def errback_httpbin(self, failure):
        """
            Error handling
        """
        # log all errback failures,
        self.logger.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            raise ValueError("Http error occured for %s" % response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
            raise ValueError("DNSLookupError error occured for %s" % response.url)
        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
            raise ValueError("TimeoutError occured for %s" % response.url)

