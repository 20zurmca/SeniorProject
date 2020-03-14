# -*- coding: utf-8 -*-

import scrapy
import sys
import re
sys.path.append('..')
from items import Player
from soccerspider import SoccerSpider
from CurrentRosterYear import get_current_roster_year
from LeagueDictionary import get_college_from_url, check_league
from TableSpider import TableSpider

class NewRosterDataTableDukeSpider(scrapy.Spider):

    """
    Spider for websites formatted like Duke's and Holy Cross's page. Only for current roster year
    """
    name = 'newRosterDataTableDukeSpider'

    current_roster_year = get_current_roster_year() #i.e 2018-2019

    custom_settings = {

            'ITEM_PIPELINES':{
                        'SoccerScrape.pipelines.IncomingPlayerPipeline': 300,
        }
     }

    start_urls = [
    'http://www.goduke.com/SportSelect.dbml?SPID=1833&SPSID=22446&DB_OEM_ID=4200',
    'https://goholycross.com/SportSelect.dbml?DB_OEM_ID=33100&SPID=174208&SPSID=1020214'
    ]

    allowed_domains = [
    'www.goduke.com',
    'goholycross.com'
    ]

    INDEX = { #maps the school to where the attributes are in the HTMl <td> tags
        'www.goduke'        :{'NUMBER': 1 ,'PLAYER_POSITION': 3, 'ACADEMIC_YEAR': 6, 'HEIGHT': 4, 'WEIGHT': 5 ,'LOCATION': 7},
        'goholycross'   :{'NUMBER': 1 ,'PLAYER_POSITION': 3, 'ACADEMIC_YEAR': 6, 'HEIGHT': 4, 'WEIGHT': 5 , 'LOCATION': 7}
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
        players_table_view = '//*[@id="roster-list-table"]/tbody/tr'
        players            = response.xpath(players_table_view)
        school_url         = response.url[response.url.index('/')+2:response.url.index('.com')] #domain for school

        roster_year        = (response.xpath('//*[@id="roster-page"]/h1/text()')
                                      .extract_first()
                                      .split(' ')[-2]
                                      .split('-')[1]
                                      .strip())

        for player in players:
            #extracting data from table
            playerItem  = Player()
            player_name = player.xpath(".//td[2]/a/text()").extract_first().strip().split() #array [fn, ln]

            if(len(player_name) == 0):
                continue #skipping header row

            player_first_name      = player_name[0].strip()
            player_last_name       = " ".join(player_name[1:]).strip()

            player_position         = player.xpath('.//td['+ self.reference_index(school_url, 'PLAYER_POSITION') + ']/text()').extract_first().strip() #'position'

            player_class_year      = player.xpath('.//td['+ self.reference_index(school_url, 'ACADEMIC_YEAR') + ']/text()').extract()[1].strip()

            player_height          = player.xpath('.//td['+ self.reference_index(school_url, 'HEIGHT') + ']/text()').extract() #array['feet-inches']

            number                 = player.xpath('.//td[' + self.reference_index(school_url, 'NUMBER') + ']/text()').extract_first().strip()

            weight                 = player.xpath('.//td[' + self.reference_index(school_url, 'WEIGHT') + ']/text()').extract_first().strip()

            if(len(player_height) == 0):
                player_height = 'NA'
            else:
                player_height = player_height[0].strip()

            player_location        = player.xpath('.//td['+ self.reference_index(school_url, 'LOCATION') + ']/text()').extract_first().strip()

            #Item Processing
            playerItem['previousSchool'] = 'NA'
            self.process_player_location(playerItem, player_location)
            playerItem['rosterYear'] = roster_year
            playerItem['college'] = get_college_from_url(urlDomain=response.url[response.url.index('/')
                                                                        + 2:response.url.index('.com')+4])

            playerItem['collegeLeague'] = check_league(urlDomain=response.url[response.url.index('/')
                                                                        + 2:response.url.index('.com')+4])

            SoccerSpider.process_other_attribute(playerItem, player_first_name, 'firstName')
            SoccerSpider.process_other_attribute(playerItem, player_last_name, 'lastName')
            SoccerSpider.process_other_attribute(playerItem, player_position, 'position')
            SoccerSpider.process_other_attribute(playerItem, player_class_year, 'classYear')
            TableSpider.process_other_attribute(playerItem, player_height, 'height')
            SoccerSpider.process_other_attribute(playerItem, number, 'number')
            SoccerSpider.process_other_attribute(playerItem, weight, 'weight')

            href                   = player.xpath('.//td[2]/a/@href').extract_first()
            link                   = response.url[0:response.url.index('.com')+4] + href

            playerItem['profileLink'] = link

            yield playerItem


    def process_player_location(self, playerItem, player_location):
        """
        method process_player_location processes attributes regarding high school, hometown, and home state
        type player_location: string formatted
        """
        if not player_location:
            playerItem['homeTown'] = 'NA'
            playerItem['state_or_country'] = 'NA'
            playerItem['highSchool'] = 'NA'
            return

        split_location = player_location.split('(')
        homeTown = split_location[0].strip().split(',') #['hometown', 'state']
        playerItem['homeTown'] = re.sub(' +', ' ', homeTown[0].strip())
        playerItem['state_or_country'] = re.sub(' +', ' ', homeTown[1].strip())
        playerItem['highSchool'] = 'NA'

        if len(split_location) > 1:
            highSchool = split_location[1].strip()
            playerItem['highSchool'] = re.sub('[)]', '', highSchool)

    @classmethod
    def reference_index(self, school_url, attribute):
        """ Method reference_index looks up the proper index value in <td> tages for the data needed"""
        return str(NewRosterDataTableDukeSpider.INDEX[school_url][attribute])


