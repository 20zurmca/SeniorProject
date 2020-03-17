leagueDict ={

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

        'AMERICAN ATHLETIC': ['Southern Methodist University'],

    }


tail.select("#collegeLeagueSelector", {
  search: true,
  multiSelectAll: true,
  placeholder: "College League",
  width: 330
});

tail.select("#collegeSelector", {
  search: true,
  multiSelectAll: true,
  placeholder: "College",
});

tail.select("#positionSelector", {
  search: true,
  multiSelectAll: true,
  placeholder: "Position",
});

tail.select("#starterSelector", {
  multiSelectAll: true,
  placeholder: "Number of Years Starter",
});

tail.select("#allConferenceSelector", {
  placeholder: "Number of Years All-Conference",
  multiSelectAll: true,
  width: 330
});
