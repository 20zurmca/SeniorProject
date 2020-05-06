leagueDict ={ #Make sure to add leagues in upper-case.

        'PATRIOT' : ['Lafayette College', 'Lehigh University', 'American University',
                      'Army West Point', 'Naval Academy', 'Boston University',
                      'Bucknell University', 'Colgate University', 'College of the Holy Cross',
                      'Loyola University Maryland'],

        'IVY'     : ['University of Pennsylvania', 'Harvard University', 'Yale University',
                     'Brown University', 'Cornell University', 'Dartmouth College', 'Columbia University',
                     'Princeton University'],

        'PAC-12'  : ['Stanford University'],

        'COLONIAL ATHLETIC ASSOCIATION' : ['Northeastern University', 'College of William & Mary'],

        'ATLANTIC COAST' : ['Boston College', 'University of Notre Dame', 'Syracuse University',
                            'Wake Forest University', 'Duke University'],

        'BIG EAST' : ['Georgetown University', 'Villanova University'],

        'A-10'     : ['Davidson College'],

        'BIG TEN'  : ['Northwestern University'],

        'SOUTHERN' : ['Furman University', 'Wofford College'],

        'WAC' : ['Air Force Academy'],

        'AMERICAN ATHLETIC': ['SMU'],
    }

def get_college_from_url(urlDomain):
        """
            Cross references a url domain to a college
        """
        switcher = {
            'www.goleopards.com'   : 'Lafayette College',
            'lehighsports.com'     : 'Lehigh University',
            'gocolgateraiders.com' : 'Colgate University',
            'goprincetontigers.com': 'Princeton University',
            'goterriers.com'       : 'Boston University',
            'bucknellbison.com'    : 'Bucknell University',
            'loyolagreyhounds.com' : 'Loyola University Maryland',
            'navysports.com'       : 'Naval Academy',
            'pennathletics.com'    : 'University of Pennsylvania',
            'brownbears.com'       : 'Brown University',
            'dartmouthsports.com'  : 'Dartmouth College',
            'gocolumbialions.com'  : 'Columbia University',
            'gostanford.com'       : 'Stanford University',
            'und.com'              : 'University of Notre Dame',
            'georgetown.sidearmsports.com' : 'Georgetown University',
            'godeacs.com'          : 'Wake Forest University',
            'bceagles.com'         : 'Boston College',
            'villanova.com'        : 'Villanova University',
            'cuse.com'             : 'Syracuse University',
            'smumustangs.com'      : 'SMU',
            'davidsonwildcats.com' : 'Davidson College',
            'goairforcefalcons.com': 'Air Force Academy',
            'woffordterriers.com'  : 'Wofford College',
            'aueagles.com'         : 'American University',
            'furmanpaladins.com'   : 'Furman University',
            'nuhuskies.com'        : 'Northeastern University',
            'yalebulldogs.com'     : 'Yale University',
            'tribeathletics.com'   : 'College of William & Mary',
            'cornellbigred.com'    : 'Cornell University',
            'goarmywestpoint.com'  : 'Army West Point',
            'www.goduke.com'       : 'Duke University',
            'goholycross.com'      : 'College of the Holy Cross',
            'gocrimson.com'        : 'Harvard University',
            'nusports.com'         : 'Northwestern University'
            }

        return switcher.get(urlDomain, 'Invalid')

def check_league(urlDomain):
        school = get_college_from_url(urlDomain)
        for key in leagueDict.keys():
            if school in leagueDict[key]: #checking through each value (list) in leagueDict to find match. If match, return key
                return key
        return 'NONE'
