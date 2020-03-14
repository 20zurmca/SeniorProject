import scrapy
import re
import sys
sys.path.append('..')
from items import Player
from soccerspider import SoccerSpider
from CurrentRosterYear import get_current_roster_year
from LeagueDictionary import get_college_from_url, check_league


class NewRosterDataTableSpider(scrapy.Spider):
    """
    Spider for a table view current roster year
    """
    name = 'newRosterDataTableSpider'

    year = get_current_roster_year() #i.e 2018-19 for the url in start_urls

    custom_settings = {

            'ITEM_PIPELINES':{
                        'SoccerScrape.pipelines.IncomingPlayerPipeline': 300,
        }
     }

    start_urls = [
    'http://www.aueagles.com/sports/m-soccer/' + year + '/roster',
    'http://www.furmanpaladins.com/sports/m-soccer/' + year + '/roster',
    'http://www.yalebulldogs.com/sports/m-soccer/'+ year + '/roster',
    ]

    allowed_domains = [
    'www.aueagles.com',
    'www.furmanpaladins.com',
    'www.yalebulldogs.com'
    ]

    INDEX = { #maps the school to where the attributes are in the HTMl <td> tags
        'aueagles' : {'NUMBER': 1, 'PLAYER_POSITION': 2, 'ACADEMIC_YEAR': 3, 'HEIGHT': 4, 'WEIGHT': 5, 'LOCATION': 6},
        'furmanpaladins': {'NUMBER': 1, 'PLAYER_POSITION': 2, 'ACADEMIC_YEAR': 3, 'HEIGHT': 4, 'WEIGHT': 5, 'LOCATION': 6},
        'yalebulldogs' : {'NUMBER': 1, 'PLAYER_POSITION': 2, 'ACADEMIC_YEAR': 3, 'HEIGHT': 4, 'WEIGHT': 5, 'LOCATION': 6},
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
        players_table_view =  '//div[@class = "roster"]/table/tbody/tr'
        players            = response.xpath(players_table_view);
        roster_year        = response.url.split('/')[-2].split('-')[0] #getting roster year from url

        for player in players:
            #extracting data from table
            player_name            = player.xpath('.//th[@class = "name"]/a/text()').extract()[1].strip().split()
            player_first_name      = player_name[0]
            player_last_name       = " ".join(player_name[1:]).strip()
            player_positon         = (player.xpath('.//td['+ self.reference_index(school_url, 'PLAYER_POSITION') + ']/text()')
                                           .extract()[1].strip())

            player_class_year      = (player.xpath('.//td['+ self.reference_index(school_url, 'ACADEMIC_YEAR') + ']/text()')
                                           .extract()[1].strip())

            player_height          = (player.xpath('.//td['+ self.reference_index(school_url, 'HEIGHT') + ']/text()')
                                           .extract()[1].strip())

            player_weight = (player.xpath('.//td['+ self.reference_index(school_url, 'WEIGHT') + ']/text()')
                                           .extract()[1].strip())

            player_number = (player.xpath('.//td['+ self.reference_index(school_url, 'NUMBER') + ']/text()')
                                           .extract()[1].strip())

            player_location        = (player.xpath('.//td['+ self.reference_index(school_url, 'LOCATION') + ']/text()')
                                           .extract()[1].split('/'))

            player_hometown        = player_location[0].strip().split(',')[0]

            player_homestate       = " ".join(player_location[0].strip().split(',')[1:])

            player_high_school     = player_location[1].strip()

            #Item Processing
            playerItem = Player()
            playerItem['previousSchool'] = 'NA' #table view does not list previous school
            playerItem['rosterYear'] = roster_year
            playerItem['college'] = get_college_from_url(urlDomain=response.url[response.url.index('www.')
                                                                        + 4:response.url.index('.com')+4])
            playerItem['collegeLeague'] = check_league(urlDomain=response.url[response.url.index('www.')
                                                                        + 4:response.url.index('.com')+4])

            href = response.xpath('.//th[@class = "name"]/a/@href').extract_first()
            link                   = response.url[0:response.url.index('.com')+4] + href

            playerItem['profileLink'] = link

            SoccerSpider.process_other_attribute(playerItem, player_first_name, 'firstName')
            SoccerSpider.process_other_attribute(playerItem, player_last_name, 'lastName')
            SoccerSpider.process_other_attribute(playerItem, player_positon, 'position')
            SoccerSpider.process_other_attribute(playerItem, player_class_year, 'classYear')
            self.process_other_attribute(playerItem, player_height, 'height')
            SoccerSpider.process_other_attribute(playerItem, player_hometown, 'homeTown')
            SoccerSpider.process_other_attribute(playerItem, player_homestate, 'state_or_country')
            SoccerSpider.process_other_attribute(playerItem, player_high_school, 'highSchool')
            SoccerSpider.process_other_attribute(playerItem, player_weight, 'weight')
            SoccerSpider.process_other_attribute(playerItem, player_number, 'number')

            yield playerItem


    @classmethod
    def reference_index(self, school_url, attribute):
        """ Method reference_index looks up the proper index value in <td> tages for the data needed"""
        return str(NewRosterDataTableSpider.INDEX[school_url][attribute])


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

