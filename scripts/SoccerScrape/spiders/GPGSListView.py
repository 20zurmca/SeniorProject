import scrapy
import sys
sys.path.append('..')
from items import Starter
from CurrentRosterYear import get_current_roster_year
from LeagueDictionary import get_college_from_url
 #Dictionary with keys of leagues, values of list of member schools


class GPGSSpider(scrapy.Spider):

    """
        A spider that parses various schools' men's soccer statistics that have websites like Lafayette's
    """
    name = "GPGSSpider"

    current_roster_year = get_current_roster_year()

    custom_settings = {
        'ITEM_PIPELINES':{
            'SoccerScrape.pipelines.StarterPipeline': 400,
      }
   }


    start_urls = [
        'https://www.goleopards.com/cumestats.aspx?path=msoc',
         'https://lehighsports.com/cumestats.aspx?path=msoc&year=' + current_roster_year.split('-')[0] +\
         '&_ga=2.12181812.1447966859.1547234959-600779335.1546536377',
        'https://gocolgateraiders.com/cumestats.aspx?path=msoc',
        'https://goprincetontigers.com/cumestats.aspx?path=msoc',
        'https://goterriers.com/cumestats.aspx?path=msoc',
        'https://bucknellbison.com/cumestats.aspx?path=msoc',
        'https://loyolagreyhounds.com/cumestats.aspx?path=msoc',
        'https://navysports.com/cumestats.aspx?path=msoc',
        'https://pennathletics.com/cumestats.aspx?path=msoc',
        'https://brownbears.com/cumestats.aspx?path=msoc',
        'https://dartmouthsports.com/cumestats.aspx?path=msoc',
        'https://gocolumbialions.com/cumestats.aspx?path=msoc',
        'https://gostanford.com/cumestats.aspx?path=msoc',
        'https://und.com/cumestats.aspx?path=msoc',
        'http://georgetown.sidearmsports.com/cumestats.aspx?path=msoc',
        'https://godeacs.com/cumestats.aspx?path=msoc',
        'https://bceagles.com/cumestats.aspx?path=msoc',
        'https://villanova.com/cumestats.aspx?path=msoc',
        'https://cuse.com/cumestats.aspx?path=msoccer',
        'https://smumustangs.com/cumestats.aspx?path=msoc',
        'https://davidsonwildcats.com/cumestats.aspx?path=msoc',
        'https://goairforcefalcons.com/cumestats.aspx?path=msoc',
        'https://woffordterriers.com/cumestats.aspx?path=msoc',
        'https://nuhuskies.com/cumestats.aspx?path=msoc',
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
        'nuhuskies.com',
    ]

    #xpath strings for a common type of format that multiple websites share
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

        potential_starts = response.xpath('//tfoot/tr[1]/td[2]')[0].xpath('./text()').extract_first()
        roster_year      = int(GPGSSpider.current_roster_year.split('-')[0])

        players = response.xpath('//table')[1].xpath('./tbody/tr')  \
                + response.xpath('//table')[2].xpath('./tbody/tr')

        for player in players:
            starterItem = Starter()
            starterItem['potentialStarts'] = potential_starts
            gpgs = player.xpath('./td/text()').extract()[1].strip() #'GamesPlayed-GamesStarted'
            name = player.xpath('./th/a/text()').extract_first().strip()
            number = player.xpath('./td/text()').extract()[0].strip()
            if '-' not in number and number is not None:
                starterItem['number'] = number
            else:
                starterItem['number'] = 'NA'

            starterItem['school'] = get_college_from_url(response.url[response.url.index('/')+2:response.url.index('.com')+4])
            starterItem['rosterYear'] = roster_year

            if gpgs:
                gp = gpgs.split('-')[0]
                gs = gpgs.split('-')[1]
                if gp and gs:
                    starterItem['starts'] = gs
                    starterItem['plays']  = gp
                    ratio_of_starts = int(gs)/int(potential_starts)
                    if ratio_of_starts >= 0.5:
                        starterItem['isStarter'] = 'Y'
                    else:
                        starterItem['isStarter'] = 'N'
                else:
                    if not gp:
                        starterItem['plays'] = 'NA'
                        starterItem['isStarter'] = 'NA'
                        starterItem['starts'] = gs
                    if not gs:
                        starterItem['starts'] = 'NA'
                        starterItem['isStarter'] = 'NA'
                        starterItem['plays'] = gp

                    starterItem['isStarter'] = 'NA'
            else:
                starterItem['plays'] = 'NA'
                starterItem['starts'] = 'NA'
                starterItem['isStarter'] = 'NA'

            try:
                firstName = name.split(',')[1]
                lastName  = name.split(',')[0]
                starterItem['firstName'] = firstName.strip()
                starterItem['lastName']  = lastName.strip()

            except: #some schools add a 'team' row in the individual tables for some reason.
                    #See 'https://loyolagreyhounds.com/cumestats.aspx?path=msoc' for example

                    if len(name.split(' ')) > 1:
                        print('Error splitting name by ,: ', name)
                    if name.lower() == 'team':
                        continue
                    else:
                        starterItem['firstName'] = name
                        starterItem['lastName']  = 'NA'

            yield starterItem


