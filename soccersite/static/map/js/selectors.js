/*
  Selectors.js provides logic for handling the selectors
*/

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

        'AMERICAN ATHLETIC': ['SMU'],

    }

//keeps track of selected leagues to assist with the effect when you select a league,
//the appropriate colleges are selected as well
priorSelectedLeagues = {'PATRIOT': false, 'IVY': false, 'PAC-12': false,
                        'COLONIAL ATHLETIC ASSOCIATION': false, 'ATLANTIC COAST': false,
                        'BIG EAST': false, 'A-10': false, 'BIG TEN': false, 'SOUTHERN': false,
                        'WAC': false, 'AMERICAN ATHLETIC': false};

//constructing selector objects
var leagueSelector = tail.select("#collegeLeagueSelector", {
  search: true,
  multiSelectAll: true,
  placeholder: "College League"
});

var collegeSelector = tail.select("#collegeSelector", {
  search: true,
  multiSelectAll: true,
  placeholder: "College",
});

var positionSelector = tail.select("#positionSelector", {
  search: true,
  multiSelectAll: true,
  placeholder: "Position",
});

var starterSelector = tail.select("#starterSelector", {
  multiSelectAll: true,
  placeholder: "Number of Years Starter",
  multiShowCount: false,
});

var allConferenceSelector = tail.select("#allConferenceSelector", {
  placeholder: "Number of Years All-Conference",
  multiSelectAll: true,
  multiShowCount: false,
});

/**
 * Functionality to selected/deselect all colleges in a selected league
*/
leagueSelector.on("change", function(){
  leagues = leagueSelector.options.items["College League"]; //dictionary of leagues
  for(var league in leagues){ //iterating over the keys
    colleges = leagueDict[league];
    if(leagues[league]['selected']){ //selection made
      if(!priorSelectedLeagues[league]){ //new selection
        colleges.forEach(function(c){
          collegeSelector.options.select(c, "College");
       });
      priorSelectedLeagues[league] = !priorSelectedLeagues[league]; //change state
    }
  } else { //unselection made
      if(priorSelectedLeagues[league]){ //undo a prior selection
        colleges.forEach(function(c){
          collegeSelector.options.unselect(c, "College");
       });
      priorSelectedLeagues[league] = !priorSelectedLeagues[league]; //change state
     }
   }
 }
});
