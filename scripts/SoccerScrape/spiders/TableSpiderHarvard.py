import scrapy
import re
import sys
sys.path.append('..')
from items import Player
from soccerspider import SoccerSpider
from CurrentRosterYear import get_current_roster_year
from LeagueDictionary import get_college_from_url, check_league


class TableSpiderHarvard(scrapy.Spider):
    """
    spider for scraping school sites like Harvard
    """
    name = 'soccerSpider5'

    year = get_current_roster_year() #i.e 2018-19 for the url in start_urls

    custom_settings = {

            'ITEM_PIPELINES':{
                        'SoccerScrape.pipelines.PlayerPipeline': 300,
        }
     }

    start_urls = [
    'https://www.gocrimson.com/sports/msoc/' + year + '/roster'

    ]

    allowed_domains = [
    'www.gocrimson.com'
    ]

    INDEX = { #maps the school to where the attributes are in the HTMl <td> tags
        'gocrimson' : {'NUMBER': 1, 'PLAYER_POSITION': 3, 'ACADEMIC_YEAR': 2, 'HEIGHT': 4, 'WEIGHT': 5, 'HOMETOWN': 6, 'HIGH_SCHOOL': 7},

    }


    def start_requests(self):
        """
            Starts the http request
        """
        for u in self.start_urls:
            try:
                yield scrapy.Request(u, callback=self.parse_list,
                errback=SoccerSpider.errback_httpbin, dont_filter=True)
            except ValueError:
                print("ValueError")
                continue


    def parse_list(self, response):
        """
            parses data in a table format similar to American University's
        """
        self.logger.debug('Got successful response from {}'.format(response.url))
        school_url         = response.url[response.url.index('.')+1:response.url.index('.com')] #domain for school
        players_table_view =  "//div[@class = 'roster']/table/tbody/tr"
        players            = response.xpath(players_table_view)
        roster_year        = response.url.split('/')[-2].split('-')[0] #getting roster year from url

        for player in players:
            #extracting data from table
            player_name            = player.xpath('.//th[@class = "name"]/a/text()').extract()[1].strip().split()
            href                   = player.xpath('.//th[@class = "name"]/a/@href').extract_first().strip()
            link                   = response.url[0:response.url.index('.com')+4] + href

            player_first_name      = player_name[0]
            player_last_name       = " ".join(player_name[1:]).strip()
            player_positon         = (player.xpath('.//td['+ self.reference_index(school_url, 'PLAYER_POSITION') + ']/text()')
                                           .extract()[1].strip())

            player_class_year      = (player.xpath('.//td['+ self.reference_index(school_url, 'ACADEMIC_YEAR') + ']/text()')
                                           .extract()[1].strip())

            player_height          = (player.xpath('.//td['+ self.reference_index(school_url, 'HEIGHT') + ']/text()')
                                           .extract()[1].strip())

            player_location        = (player.xpath('.//td['+ self.reference_index(school_url, 'HOMETOWN') + ']/text()')
                                           .extract()[1])

            player_hometown        = player_location.strip().split(',')[0].strip()
            player_homestate       = re.sub(' +', ' '," ".join(player_location.strip().split(',')[1:]))

            player_high_school     = (player.xpath('.//td['+ self.reference_index(school_url, 'HIGH_SCHOOL') + ']/text()')
                                           .extract()[1].strip())

            number                 = (player.xpath('.//td['+ self.reference_index(school_url, 'NUMBER') + ']/text()')
                                           .extract()[1].strip())

            weight                 = (player.xpath('.//td['+ self.reference_index(school_url, 'WEIGHT') + ']/text()')
                                           .extract()[1].strip())

            #Item Processing
            playerItem = Player()
            playerItem['previousSchool'] = 'NA' #table view does not list previous school
            playerItem['rosterYear']     = roster_year
            playerItem['college']        = get_college_from_url(urlDomain=response.url[response.url.index('www.')
                                                                        + 4:response.url.index('.com')+4])
            playerItem['collegeLeague']  = check_league(urlDomain=response.url[response.url.index('www.')
                                                                        + 4:response.url.index('.com')+4])

            playerItem['profileLink']    = link

            SoccerSpider.process_other_attribute(playerItem, player_first_name, 'firstName')
            SoccerSpider.process_other_attribute(playerItem, player_last_name, 'lastName')
            SoccerSpider.process_other_attribute(playerItem, player_positon, 'position')
            SoccerSpider.process_other_attribute(playerItem, player_class_year, 'classYear')
            self.process_other_attribute(playerItem, player_height, 'height')
            SoccerSpider.process_other_attribute(playerItem, player_hometown, 'homeTown')
            SoccerSpider.process_other_attribute(playerItem, player_homestate, 'state_or_country')
            SoccerSpider.process_other_attribute(playerItem, player_high_school, 'highSchool')
            SoccerSpider.process_other_attribute(playerItem, number, 'number')
            SoccerSpider.process_other_attribute(playerItem, weight, 'weight')

            yield playerItem

            pages_to_visit = [] #acquire pages to visit
            starting_year  = int(TableSpiderHarvard.year.split('-')[0]) #current starting roster year
            ending_year    = int(TableSpiderHarvard.year.split('-')[1])
            while(starting_year > 2006):
                starting_year -= 1
                ending_year   -= 1

                if len(str(ending_year)) != 1: #ie 10
                    year = str(starting_year) +  '-' + str(ending_year)
                else:
                    year= str(starting_year) + '-' + '0' + str(ending_year) #append zero to i.e 9 to make 09

                index_of_current_roster_year = re.search('\d', response.url).start() #finding index of the roster year in url
                length_of_current_roster_year = len(TableSpiderHarvard.year) #length of the string

                pages_to_visit.append(response.url[0:index_of_current_roster_year] #rebuild url
                                        + year + response.url[index_of_current_roster_year
                                                                     + length_of_current_roster_year:])

            for url in pages_to_visit:
                yield scrapy.Request(url = url, callback=self.parse_list)



    @classmethod
    def reference_index(self, school_url, attribute):
        """ Method reference_index looks up the proper index value in <td> tages for the data needed"""
        return str(TableSpiderHarvard.INDEX[school_url][attribute])


    @classmethod
    def process_other_attribute(self, player, attribute, attributeName):
        """
            Processes a generic attribute for player item from table
        """
        if(attribute is None or attribute.isspace() or attribute == '' or attribute == '-'):
            player[attributeName] = 'NA'
            return
        else:
            if(attributeName == 'height'):
                player[attributeName] = re.sub('-', "'", attribute)
                return
            player[attributeName] = attribute.strip()

        player[attributeName] = re.sub(' +', ' ', player[attributeName])



