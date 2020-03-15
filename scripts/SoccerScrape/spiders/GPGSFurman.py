import scrapy
import sys
import re
sys.path.append('..')
from items import Starter
from CurrentRosterYear import get_current_roster_year
from LeagueDictionary import get_college_from_url
 #Dictionary with keys of leagues, values of list of member schools


class GPGSFurman(scrapy.Spider):

    name = 'GPGSSpiderFurman'

    year = get_current_roster_year() #i.e 2018-19 for the url in start_urls

    custom_settings = {

            'ITEM_PIPELINES':{
                        'SoccerScrape.pipelines.StarterPipeline': 400,
        }
     }

    start_urls = [
     'http://www.furmanpaladins.com/sports/m-soccer/' + year + '/files/teamcume.htm'
    ]

    allowed_domains = [
    'www.furmanpaladins.com'

    ]

    def start_requests(self):
        """
            Starts the http request
        """
        for u in self.start_urls:
            try:
                yield scrapy.Request(u, callback=self.parse_list, dont_filter=True)
            except ValueError:
                print("ValueError")
                continue

    def parse_list(self, response):

        self.logger.debug('Got successful response from {}'.format(response.url))

        potential_starts = self.get_potential_starts(response)
        roster_year      = int(GPGSFurman.year.split('-')[0])

        players = self.get_players(response)

        for player in players:
            starterItem = Starter()
            name = self.get_player_name(player)

            if name is None:
                continue
            else:
                name = re.sub(' +', ',', name.strip())
            try:
                firstName = name.split(',')[0]
                lastName  = name.split(',')[1]
                starterItem['firstName'] = firstName.strip()
                starterItem['lastName']  = lastName.strip()

            except:

                if len(name.split(' ')) > 1:
                    print('Error splitting name by space: ', name)
                if name.lower() in ['team', 'totals', 'opponent']:
                    continue
                else:
                    starterItem['firstName'] = name
                    starterItem['lastName']  = 'NA'

            starterItem['potentialStarts'] = potential_starts
            gp = self.get_gp(player).strip()
            gs = self.get_gs(player).strip()
            number = self.get_number(player)
            if '-' not in number and number is not None:
                starterItem['number'] = number
            else:
                starterItem['number'] = 'NA'

            starterItem['school'] = get_college_from_url(response.url[response.url.index('.')+1:response.url.index('.com')+4])
            starterItem['rosterYear'] = roster_year

            if gp and gs:
                gp_set_na = False
                gs_set_na = False
                if gp.strip() == '-':
                    starterItem['plays'] = 'NA'
                    gp_set_na = True
                if gs.strip() == '-':
                    starterItem['starts'] = 'NA'
                    gs_set_na = True
                if not gs_set_na:
                    starterItem['starts'] = gs
                if not gp_set_na:
                    starterItem['plays']  = gp

                if not gp_set_na and not gs_set_na:
                    ratio_of_starts = float(int(gs)/int(potential_starts))

                    if ratio_of_starts >= 0.5:
                        starterItem['isStarter'] = 'Y'

                    else:
                        starterItem['isStarter'] = 'N'
                else:
                    starterItem['isStarter'] = 'NA'
            else:

                    starterItem['isStarter'] = 'NA'

            yield starterItem

    def get_potential_starts(self, response):
        return response.xpath('//table[4]/tr[@bgcolor = "#ffffff"]')[2:-3][-1].xpath('./td/font/text()')[2] \
                                                                                                    .extract() \
                                                                                                    .strip()
    def get_players(self, response):
        return response.xpath('//table[4]/tr[@bgcolor = "#ffffff"]')[2:-4]

    def get_player_name(self, player):
        return player.xpath('./td[2]/font/text()').extract_first().strip()

    def get_gp(self, player):
        return player.xpath('./td[3]/font/text()').extract_first().strip().split('-')[0]

    def get_gs(self, player):
       return player.xpath('./td[3]/font/text()').extract_first().strip().split('-')[1]

    def get_number(self, player):
        return player.xpath('./td[1]/font/text()').extract_first().strip()








