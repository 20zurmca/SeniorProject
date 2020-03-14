import scrapy
import sys
import re
sys.path.append('..')
from items import Starter
from CurrentRosterYear import get_current_roster_year
from LeagueDictionary import get_college_from_url
 #Dictionary with keys of leagues, values of list of member schools


class GPGSAmericanUniversity(scrapy.Spider):

    name = 'GPGSSpiderAmerican'

    year = get_current_roster_year() #i.e 2018-19 for the url in start_urls

    custom_settings = {

            'ITEM_PIPELINES':{
                        'SoccerScrape.pipelines.StarterPipeline': 400,
        }
     }

    start_urls = [
     'http://www.aueagles.com/sports/m-soccer/' + year + '/teams/american?view=lineup&r=0&pos=kickers',
     'http://www.yalebulldogs.com/sports/m-soccer/' + year + '/teams/yale?view=lineup&r=0&pos=kickers',
     'https://www.gocrimson.com/sports/msoc/' + year +'/teams/harvard?view=lineup&r=0&pos=kickers'
    ]

    allowed_domains = [
    'www.aueagles.com',
    'www.yalebulldogs.com',
    'www.gocrimson.com'
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
        roster_year      = int(GPGSAmericanUniversity.year.split('-')[0])

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
            if number is not None:
                if '-' in number:
                    starterItem['number'] = 'NA'
                else:
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
                    ratio_of_starts = int(gs)/int(potential_starts)

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
        if response.url == 'http://www.aueagles.com/sports/m-soccer/' \
                  + GPGSAmericanUniversity.year + '/teams/american?view=lineup&r=0&pos=kickers':

            return response.xpath('//*[@id="mainbody"]/div[1]/div[2]/div[2]/div[2]/div/div[2] \
                                   /div[1]/div/div[2]/div[2]/div[2]/div/div/div/table/tr[31] \
                                   /td[5]/text()').extract_first().strip()

        elif response.url == 'http://www.yalebulldogs.com/sports/m-soccer/' \
                    + GPGSAmericanUniversity.year + '/teams/yale?view=lineup&r=0&pos=kickers':

            return  response.xpath('//*[@id="mainbody"]/div[1]/div[2]/div[2]/div[2]/div/div[2] \
                                   /div[1]/div/div[2]/div[2]/div[2]/div/div/div/table/tr[34] \
                                   /td[5]/text()').extract_first().strip()

        elif response.url == 'https://www.gocrimson.com/sports/msoc/' \
                    + GPGSAmericanUniversity.year + '/teams/harvard?view=lineup&r=0&pos=kickers':

            return response.xpath('//*[@id="mainbody"]/div[1]/div[2]/div[2]/div[2]/div/div[2] \
                                  /div[1]/div/div[2]/div[2]/div[2]/div/div/div/table/tr[27] \
                                  /td[5]/text()').extract_first().strip()

        return 'Error in GSGPAmerican.py-get_potential_starts'

    def get_players(self, response):
        return response.xpath("//div[@class = 'scrollable']/div/table")[0].xpath('./tr')[1:-2] \
                                + response.xpath("//div[@class = 'scrollable']/div/table")[1].xpath('./tr')[1:-2]

    def get_player_name(self, player):
        return player.xpath('./td[2]/a/text()').extract_first()

    def get_gp(self, player):
        return player.xpath('./td[5]/text()').extract_first()

    def get_gs(self, player):
        return player.xpath('./td[6]/text()').extract_first()

    def get_number(self, player):
        return player.xpath('./td[1]/text()').extract_first()








