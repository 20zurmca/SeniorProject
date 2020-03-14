import scrapy
import sys
import re
sys.path.append('..')
from items import Player
from soccerspider import SoccerSpider
from LeagueDictionary import get_college_from_url, check_league
from TableSpider import TableSpider

class NewRosterDataTableWMSpider(scrapy.Spider):

    """
    Spider for websites formatted like William and Mary's page
    Includes W&M, Cornell, Army. Only current roster year
    """
    name = 'newRosterDataTableWMSpider'

    start_urls = [
     'https://tribeathletics.com/roster.aspx?path=msoc',
     'https://cornellbigred.com/roster.aspx?path=msoccer',
     'https://goarmywestpoint.com/roster.aspx?path=msoc',
     'https://nusports.com/roster.aspx?path=msoc'
    ]

    allowed_domains = [
    'tribeathletics.com',
    'cornellbigred.com',
    'goarmywestpoint.com',
    'nusports.com'
    ]

    custom_settings = {

            'ITEM_PIPELINES':{
                        'SoccerScrape.pipelines.IncomingPlayerPipeline': 300,
        }
     }

    INDEX = { #maps the school to where the attributes are in the HTMl <td> tags
        'tribeathletics'  :{'NUMBER': 1, 'PLAYER_POSITION': 3, 'ACADEMIC_YEAR': 6, 'HEIGHT': 4, 'WEIGHT': 5, 'LOCATION': 7},
        'cornellbigred'   :{'NUMBER': 1, 'PLAYER_POSITION': 3, 'ACADEMIC_YEAR': 6, 'HEIGHT': 4, 'WEIGHT': 5,'LOCATION': 7},
        'goarmywestpoint' :{'NUMBER': 1, 'PLAYER_POSITION': 3, 'ACADEMIC_YEAR': 4, 'HEIGHT': 5, 'WEIGHT': 6,'LOCATION': 7},
        'nusports'        :{'NUMBER': 1, 'PLAYER_POSITION': 3, 'ACADEMIC_YEAR': 6, 'HEIGHT': 4, 'WEIGHT': 5,'LOCATION': 7}
    }

    ARMY_ALTERNATIVE_INDEX = {'NUMBER': 1,'PLAYER_POSITION': 4, 'ACADEMIC_YEAR': 5, 'HEIGHT': 6, 'WEIGHT': 7,'LOCATION': 8}
    #alternative index needed for years other than 2014-2016 for army since captains are reported those years



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
        players_table_view = '//*[@id="ctl00_cplhMainContent_dgrdRoster"]/tr'
        players            = response.xpath(players_table_view);
        school_url  = response.url[response.url.index('/')+2:response.url.index('.com')] #domain for school

        roster_year        = (response.xpath("//div[@id='ctl00_divPageTitle']/h1/text()")
                                      .extract_first()
                                      .split(" ")[0])

        for player in players:
            #extracting data from table
            playerItem  = Player()
            player_name = player.xpath(".//td['@class = roster_dgrd_full_name']/a/text()").extract() #array [fn, ln]

            if(len(player_name) == 0):
                continue #skipping header row

            player_first_name  = player_name[0].strip()
            player_last_name   = " ".join(player_name[1:]).strip()

            player_position    = player.xpath('.//td['+ self.reference_index(school_url, 'PLAYER_POSITION', roster_year) + ']/text()').extract_first().strip() #'position'

            player_class_year  = player.xpath('.//td['+ self.reference_index(school_url, 'ACADEMIC_YEAR', roster_year) + ']/text()').extract_first().strip()

            player_height      = player.xpath('.//td['+ self.reference_index(school_url, 'HEIGHT', roster_year) + ']/nobr/text()').extract() #array['feet-inches']

            if(len(player_height) == 0):
                player_height = 'NA'
            else:
                player_height = player_height[0].strip()

            player_location    = player.xpath('.//td['+ self.reference_index(school_url, 'LOCATION', roster_year) + ']/text()').extract_first().strip().split("/")

            number             = player.xpath('.//td['+ self.reference_index(school_url, 'NUMBER', roster_year) + ']/text()').extract_first().strip()

            weight             = player.xpath('.//td['+ self.reference_index(school_url, 'WEIGHT', roster_year) + ']/text()').extract_first().strip()

            #Item Processing
            playerItem['college'] = get_college_from_url(urlDomain=response.url[response.url.index('/')
                                                                        + 2:response.url.index('.com')+4])
            playerItem['previousSchool'] = 'NA'
            self.process_player_location(playerItem, player_location)
            playerItem['rosterYear'] = roster_year

            playerItem['collegeLeague'] = check_league(urlDomain=response.url[response.url.index('/')
                                                                        + 2:response.url.index('.com')+4])

            href = player.xpath(".//td['@class = roster_dgrd_full_name']/a/@href").extract_first().strip()
            link = response.url[0:response.url.index('.com')+4] + href

            playerItem['profileLink']   = link

            SoccerSpider.process_other_attribute(playerItem, player_first_name, 'firstName')
            SoccerSpider.process_other_attribute(playerItem, player_last_name, 'lastName')
            SoccerSpider.process_other_attribute(playerItem, player_position, 'position')
            SoccerSpider.process_other_attribute(playerItem, player_class_year, 'classYear')
            TableSpider.process_other_attribute(playerItem, player_height, 'height')
            SoccerSpider.process_other_attribute(playerItem, number, 'number')
            SoccerSpider.process_other_attribute(playerItem, weight, 'weight')

            yield playerItem


    def process_player_location(self, playerItem, player_location):
        """
        method process_player_location processes attributes regarding high school, hometown, and home state
        type player_location: array formatted ['hometown, state'/ 'high school']
        """
        if len(player_location) == 0:
            playerItem['homeTown'] = 'NA'
            playerItem['state_or_country'] = 'NA'
            playerItem['highSchool'] = 'NA'
            return

        elif len(player_location) >= 1:
            player_hometown  = player_location[0].strip().split(',')[0]
            player_homestate = " ".join(player_location[0].strip().split(',')[1:])

            playerItem['homeTown'] = player_hometown
            playerItem['state_or_country'] =re.sub(' +', ' ', player_homestate)

            if len(player_location) == 1:
                playerItem['highSchool'] = 'NA'
            else:
                high_school = player_location[1]
                playerItem['highSchool'] = re.sub(' +', ' ', high_school)
                if not playerItem['highSchool']:
                    playerItem['highSchool'] = 'NA'
                if '(' in playerItem['highSchool'] and playerItem['college'] == 'Army West Point':
                    playerItem['previousSchool'] = re.sub('[)]', '', playerItem['highSchool'].split('(')[-1])
                    playerItem['highSchool'] = " ".join(playerItem['highSchool'].split('(')[0:-1])




    @classmethod
    def reference_index(self, school_url, attribute, rosterYear):
        """ Method reference_index looks up the proper index value in <td> tages for the data needed"""
        army_special_years = ['2014', '2015', '2016']

        if school_url == 'goarmywestpoint' and rosterYear not in army_special_years:
            return str(NewRosterDataTableWMSpider.ARMY_ALTERNATIVE_INDEX[attribute])

        return str(NewRosterDataTableWMSpider.INDEX[school_url][attribute])

