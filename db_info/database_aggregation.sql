#Database Aggregation



#Goal 1, Step 1

CREATE TABLE roster_starter_data AS (
	SELECT roster_data.Roster_Year, roster_data.Player_Number, roster_data.First_Name, roster_data.Last_Name, roster_data.Year, roster_data.Position1, roster_data.Position2, roster_data.Position3, roster_data.Height, roster_data.Weight, roster_data.Home_Town, roster_data.State_or_Country, roster_data.High_School, roster_data.Alternative_School, roster_data.College, roster_data.College_League, roster_data.Bio_Link, starter_data.Potential_Starts, starter_data.GP, starter_data.GS, starter_data.Is_Starter 
	FROM roster_data 
	LEFT JOIN starter_data 
	ON roster_data.First_Name = starter_data.First_Name, roster_data.Last_Name = starter_data.Last_Name, roster_data.Roster_Year = starter_data.Roster_Year, roster_data.College = starter_data.College
);


#Goal 1, Step 2

CREATE TABLE roster_master_data AS (
	SELECT roster_data.Roster_Year, roster_data.Player_Number, roster_data.First_Name, roster_data.Last_Name, roster_data.Year, roster_data.Position1, roster_data.Position2, roster_data.Position3, roster_data.Height, roster_data.Weight, roster_data.Home_Town, roster_data.State_or_Country, roster_data.High_School, roster_data.Alternative_School, roster_data.College, roster_data.College_League, roster_data.Bio_Link, starter_data.Potential_Starts, starter_data.GP, starter_data.GS, starter_data.Is_Starter, acollade_data.Accolade 
	FROM roster_starter_data 
	LEFT JOIN accolade_data 
	ON roster_data.First_Name = accolade_data.First_Name, roster_data.Last_Name = accolade_data.Last_Name, roster_data.Roster_Year = accolade_data.Roster_Year, roster_data.College = accolade_data.College
);


#Goal 1, Step 3

DROP TABLE roster_data;
DROP TABLE starter_data;
DROP TABLE accolade_data;
DROP TABLE roster_starter_data;


#Goal 1, Step 4

ALTER TABLE roster_master_data RENAME COLUMN roster_data.Roster_Year TO Roster_Year;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.First_Name TO First_Name;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Last_Name TO Last_Name;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Year TO Year;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Position1 TO Position1;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Position2 TO Position2;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Position3 TO Position3;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Height TO Height;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Weight TO Weight;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Home_Town TO Home_Town;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.State_or_Country TO State_or_Country;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.High_School TO High_School;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Alternative_School TO Alternative_School;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.College TO College;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.College_League TO College_Leaguel;
ALTER TABLE roster_master_data RENAME COLUMN roster_data.Bio_Link TO Bio_Link;
ALTER TABLE roster_master_data RENAME COLUMN starter_data.Potential_Starts TO Potential_Starts;
ALTER TABLE roster_master_data RENAME COLUMN starter_data.GP TO GP;
ALTER TABLE roster_master_data RENAME COLUMN starter_data.GS TO GS;
ALTER TABLE roster_master_data RENAME COLUMN starter_data.Is_Starter TO Is_Starter;
ALTER TABLE roster_master_data RENAME COLUMN acollade_data.Accolade TO Accolade;


#Goal 2, Step 1

CREATE TABLE starter_years_roster AS (
	SELECT temp4b.First_Name, temp4b.Last_Name, temp4b.Home_Town, temp4b.State_or_Country, temp4b.College, temp4b.Is_Starter_Freshman, temp4b.Is_Starter_Sophomore, temp4b.Is_Starter_Junior, temp4b.Is_Starter_Senior, temp5.Is_Starter_Graduate
	FROM (
		SELECT temp3b.First_Name, temp3b.Last_Name, temp3b.Home_Town, temp3b.State_or_Country, temp3b.College, temp3b.Is_Starter_Freshman, temp3b.Is_Starter_Sophomore, temp3b.Is_Starter_Junior, temp4.Is_Starter_Senior
		FROM (
			SELECT temp2b.First_Name, temp2b.Last_Name, temp2b.Home_Town, temp2b.State_or_Country, temp2b.College, temp2b.Is_Starter_Freshman, temp2b.Is_Starter_Sophomore, temp3.Is_Starter_Junior
			FROM (
				SELECT temp1.First_Name, temp1.Last_Name, temp1.Home_Town, temp1.State_or_Country, temp1.College, temp1.Is_Starter_Freshman, temp2.Is_Starter_Sophomore
				FROM (
					SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Is_Starter AS Is_Starter_Freshman
					FROM roster_master_data
					WHERE Year = 'Freshman'
				) AS temp1
				JOIN (
					SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Is_Starter AS Is_Starter_Sophomore
					FROM roster_master_data
					WHERE Year = 'Sophomore'
				) AS temp2
				ON temp1.First_Name=temp2.First_Name AND temp1.Last_Name=temp2.Last_Name AND temp1.Home_Town=temp2.Home_Town AND temp1.State_or_Country=temp2.State_or_Country AND temp1.College=temp2.College
			) AS temp2b
			JOIN (
				SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Is_Starter AS Is_Starter_Junior 
				FROM roster_master_data 
				WHERE Year = 'Junior'
			) AS temp3 
			ON temp2b.First_Name=temp3.First_Name AND temp2b.Last_Name=temp3.Last_Name AND temp2b.Home_Town=temp3.Home_Town AND temp2b.State_or_Country=temp3.State_or_Country AND temp2b.College=temp3.College
		) AS temp3b 
		JOIN (
			SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Is_Starter AS Is_Starter_Senior 
			FROM roster_master_data 
			WHERE Year = 'Senior'
		) AS temp4 
		ON temp3b.First_Name=temp4.First_Name AND temp3b.Last_Name=temp4.Last_Name AND temp3b.Home_Town=temp4.Home_Town AND temp3b.State_or_Country=temp4.State_or_Country AND temp3b.College=temp4.College
	) AS temp4b 
	JOIN (
		SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Is_Starter AS Is_Starter_Graduate 
		FROM roster_master_data 
		WHERE Year = 'Graduate'
	) AS temp5 
	ON temp4b.First_Name=temp5.First_Name AND temp4b.Last_Name=temp5.Last_Name AND temp4b.Home_Town=temp5.Home_Town AND temp4b.State_or_Country=temp5.State_or_Country AND temp4b.College=temp5.College
);


#Goal 2, Step 2

CREATE TABLE starter_count_roster AS (
	SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, count(Is_Starter) AS Starter_Count 
	FROM roster_master_data 
	WHERE Is_Starter = 'y'
	GROUP BY First_Name, Last_Name, Home_Town, State_or_Country, College
);


#Goal 2, Step 3

CREATE TABLE height_roster AS (
	SELECT temp4b.First_Name, temp4b.Last_Name, temp4b.Home_Town, temp4b.State_or_Country, temp4b.College, temp4b.Height_Freshman, temp4b.Height_Sophomore, temp4b.Height_Junior, temp4b.Height_Senior, temp5.Height_Graduate
	FROM (
		SELECT temp3b.First_Name, temp3b.Last_Name, temp3b.Home_Town, temp3b.State_or_Country, temp3b.College, temp3b.Height_Freshman, temp3b.Height_Sophomore, temp3b.Height_Junior, temp4.Height_Senior
		FROM (
			SELECT temp2b.First_Name, temp2b.Last_Name, temp2b.Home_Town, temp2b.State_or_Country, temp2b.College, temp2b.Height_Freshman, temp2b.Height_Sophomore, temp3.Height_Junior
			FROM (
				SELECT temp1.First_Name, temp1.Last_Name, temp1.Home_Town, temp1.State_or_Country, temp1.College, temp1.Height_Freshman, temp2.Height_Sophomore
				FROM (
					SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Height AS Height_Freshman
					FROM roster_master_data
					WHERE Year = 'Freshman'
				) AS temp1
				JOIN (
					SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Height AS Height_Sophomore
					FROM roster_master_data
					WHERE Year = 'Sophomore'
				) AS temp2
				ON temp1.First_Name=temp2.First_Name AND temp1.Last_Name=temp2.Last_Name AND temp1.Home_Town=temp2.Home_Town AND temp1.State_or_Country=temp2.State_or_Country AND temp1.College=temp2.College
			) AS temp2b
			JOIN (
				SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Height AS Height_Junior 
				FROM roster_master_data 
				WHERE Year = 'Junior'
			) AS temp3 
			ON temp2b.First_Name=temp3.First_Name AND temp2b.Last_Name=temp3.Last_Name AND temp2b.Home_Town=temp3.Home_Town AND temp2b.State_or_Country=temp3.State_or_Country AND temp2b.College=temp3.College
		) AS temp3b 
		JOIN (
			SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Height AS Height_Senior 
			FROM roster_master_data 
			WHERE Year = 'Senior'
		) AS temp4 
		ON temp3b.First_Name=temp4.First_Name AND temp3b.Last_Name=temp4.Last_Name AND temp3b.Home_Town=temp4.Home_Town AND temp3b.State_or_Country=temp4.State_or_Country AND temp3b.College=temp4.College
	) AS temp4b 
	JOIN (
		SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Height AS Height_Graduate 
		FROM roster_master_data 
		WHERE Year = 'Graduate'
	) AS temp5 
	ON temp4b.First_Name=temp5.First_Name AND temp4b.Last_Name=temp5.Last_Name AND temp4b.Home_Town=temp5.Home_Town AND temp4b.State_or_Country=temp5.State_or_Country AND temp4b.College=temp5.College
);


#Goal 2, Step 4
CREATE TABLE weight_roster AS (
	SELECT temp4b.First_Name, temp4b.Last_Name, temp4b.Home_Town, temp4b.State_or_Country, temp4b.College, temp4b.Weight_Freshman, temp4b.Weight_Sophomore, temp4b.Weight_Junior, temp4b.Weight_Senior, temp5.Weight_Graduate
	FROM (
		SELECT temp3b.First_Name, temp3b.Last_Name, temp3b.Home_Town, temp3b.State_or_Country, temp3b.College, temp3b.Weight_Freshman, temp3b.Weight_Sophomore, temp3b.Weight_Junior, temp4.Weight_Senior
		FROM (
			SELECT temp2b.First_Name, temp2b.Last_Name, temp2b.Home_Town, temp2b.State_or_Country, temp2b.College, temp2b.Weight_Freshman, temp2b.Weight_Sophomore, temp3.Weight_Junior
			FROM (
				SELECT temp1.First_Name, temp1.Last_Name, temp1.Home_Town, temp1.State_or_Country, temp1.College, temp1.Weight_Freshman, temp2.Weight_Sophomore
				FROM (
					SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Weight AS Weight_Freshman
					FROM roster_master_data
					WHERE Year = 'Freshman'
				) AS temp1
				JOIN (
					SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Weight AS Weight_Sophomore
					FROM roster_master_data
					WHERE Year = 'Sophomore'
				) AS temp2
				ON temp1.First_Name=temp2.First_Name AND temp1.Last_Name=temp2.Last_Name AND temp1.Home_Town=temp2.Home_Town AND temp1.State_or_Country=temp2.State_or_Country AND temp1.College=temp2.College
			) AS temp2b
			JOIN (
				SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Weight AS Weight_Junior 
				FROM roster_master_data 
				WHERE Year = 'Junior'
			) AS temp3 
			ON temp2b.First_Name=temp3.First_Name AND temp2b.Last_Name=temp3.Last_Name AND temp2b.Home_Town=temp3.Home_Town AND temp2b.State_or_Country=temp3.State_or_Country AND temp2b.College=temp3.College
		) AS temp3b 
		JOIN (
			SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Weight AS Weight_Senior 
			FROM roster_master_data 
			WHERE Year = 'Senior'
		) AS temp4 
		ON temp3b.First_Name=temp4.First_Name AND temp3b.Last_Name=temp4.Last_Name AND temp3b.Home_Town=temp4.Home_Town AND temp3b.State_or_Country=temp4.State_or_Country AND temp3b.College=temp4.College
	) AS temp4b 
	JOIN (
		SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Weight AS Weight_Graduate 
		FROM roster_master_data 
		WHERE Year = 'Graduate'
	) AS temp5 
	ON temp4b.First_Name=temp5.First_Name AND temp4b.Last_Name=temp5.Last_Name AND temp4b.Home_Town=temp5.Home_Town AND temp4b.State_or_Country=temp5.State_or_Country AND temp4b.College=temp5.College
);


#Goal 2, Step 5
CREATE TABLE accolade_roster AS (
	SELECT temp4b.First_Name, temp4b.Last_Name, temp4b.Home_Town, temp4b.State_or_Country, temp4b.College, temp4b.Accolade_Freshman, temp4b.Accolade_Sophomore, temp4b.Accolade_Junior, temp4b.Accolade_Senior, temp5.Accolade_Graduate
	FROM (
		SELECT temp3b.First_Name, temp3b.Last_Name, temp3b.Home_Town, temp3b.State_or_Country, temp3b.College, temp3b.Accolade_Freshman, temp3b.Accolade_Sophomore, temp3b.Accolade_Junior, temp4.Accolade_Senior
		FROM (
			SELECT temp2b.First_Name, temp2b.Last_Name, temp2b.Home_Town, temp2b.State_or_Country, temp2b.College, temp2b.Accolade_Freshman, temp2b.Accolade_Sophomore, temp3.Accolade_Junior
			FROM (
				SELECT temp1.First_Name, temp1.Last_Name, temp1.Home_Town, temp1.State_or_Country, temp1.College, temp1.Accolade_Freshman, temp2.Accolade_Sophomore
				FROM (
					SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Accolade AS Accolade_Freshman
					FROM roster_master_data
					WHERE Year = 'Freshman'
				) AS temp1
				JOIN (
					SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Accolade AS Accolade_Sophomore
					FROM roster_master_data
					WHERE Year = 'Sophomore'
				) AS temp2
				ON temp1.First_Name=temp2.First_Name AND temp1.Last_Name=temp2.Last_Name AND temp1.Home_Town=temp2.Home_Town AND temp1.State_or_Country=temp2.State_or_Country AND temp1.College=temp2.College
			) AS temp2b
			JOIN (
				SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Accolade AS Accolade_Junior 
				FROM roster_master_data 
				WHERE Year = 'Junior'
			) AS temp3 
			ON temp2b.First_Name=temp3.First_Name AND temp2b.Last_Name=temp3.Last_Name AND temp2b.Home_Town=temp3.Home_Town AND temp2b.State_or_Country=temp3.State_or_Country AND temp2b.College=temp3.College
		) AS temp3b 
		JOIN (
			SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Accolade AS Accolade_Senior 
			FROM roster_master_data 
			WHERE Year = 'Senior'
		) AS temp4 
		ON temp3b.First_Name=temp4.First_Name AND temp3b.Last_Name=temp4.Last_Name AND temp3b.Home_Town=temp4.Home_Town AND temp3b.State_or_Country=temp4.State_or_Country AND temp3b.College=temp4.College
	) AS temp4b 
	JOIN (
		SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Accolade AS Accolade_Graduate 
		FROM roster_master_data 
		WHERE Year = 'Graduate'
	) AS temp5 
	ON temp4b.First_Name=temp5.First_Name AND temp4b.Last_Name=temp5.Last_Name AND temp4b.Home_Town=temp5.Home_Town AND temp4b.State_or_Country=temp5.State_or_Country AND temp4b.College=temp5.College
);


#Goal 2, Step 6

CREATE TABLE bio_link_roster AS (
	SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Bio_Link
	FROM (
		SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, MAX(Roster_Year) as Roster_Year 
		FROM roster_master_data 
		GROUP BY First_Name, Last_Name, Home_Town, State_or_Country, College
	) AS temp1 
	JOIN roster_master_data
	ON temp1.First_Name=roster_master_data.First_Name AND temp1.Last_Name=roster_master_data.Last_Name AND temp1.Home_Town=roster_master_data.Home_Town AND temp1.State_or_Country=roster_master_data.State_or_Country AND temp1.College=roster_master_data.College AND temp1.Roster_Year=roster_master_data.Roster_Year
);


#Goal 2, Step 7

CREATE TABLE final_roster_data AS ( 
	SELECT temp4.First_Name, temp4.Last_Name, temp4.Home_Town, temp4.State_or_Country, temp4.College, temp4.Starter_Count, temp4.Is_Starter_Freshman, temp4.Is_Starter_Sophomore, temp4.Is_Starter_Junior, temp4.Is_Starter_Senior, temp4.Is_Starter_Senior, temp4.Is_Starter_Graduate, temp4.Height_Freshman, temp4.Height_Sophomore, temp4.Height_Junior, temp4.Height_Senior, temp4.Height_Graduate, temp4.Weight_Freshman, temp4.Weight_Sophomore, temp4.Weight_Junior, temp4.Weight_Senior, temp4.Weight_Graduate, temp4.Accolade_Freshman, temp4.Accolade_Sophomore, temp4.Accolade_Junior, temp4.Accolade_Senior, temp4.Accolade_Graduate, bio_link_roster.Bio_Link
	FROM (
		SELECT temp3.First_Name, temp3.Last_Name, temp3.Home_Town, temp3.State_or_Country, temp3.College, starter_count_roster.Starter_Count, temp3.Is_Starter_Freshman, temp3.Is_Starter_Sophomore, temp3.Is_Starter_Junior, temp3.Is_Starter_Senior, temp3.Is_Starter_Senior, temp3.Is_Starter_Graduate, temp3.Height_Freshman, temp3.Height_Sophomore, temp3.Height_Junior, temp3.Height_Senior, temp3.Height_Graduate, temp3.Weight_Freshman, temp3.Weight_Sophomore, temp3.Weight_Junior, temp3.Weight_Senior, temp3.Weight_Graduate, temp3.Accolade_Freshman, temp3.Accolade_Sophomore, temp3.Accolade_Junior, temp3.Accolade_Senior, temp3.Accolade_Graduate
		FROM (
			SELECT temp2.First_Name, temp2.Last_Name, temp2.Home_Town, temp2.State_or_Country, temp2.College, temp2.Is_Starter_Freshman, temp2.Is_Starter_Sophomore, temp2.Is_Starter_Junior, temp2.Is_Starter_Senior, temp2.Is_Starter_Senior, temp2.Is_Starter_Graduate, temp2.Height_Freshman, temp2.Height_Sophomore, temp2.Height_Junior, temp2.Height_Senior, temp2.Height_Graduate, temp2.Weight_Freshman, temp2.Weight_Sophomore, temp2.Weight_Junior, temp2.Weight_Senior, temp2.Weight_Graduate, accolade_roster.Accolade_Freshman, accolade_roster.Accolade_Sophomore, accolade_roster.Accolade_Junior, accolade_roster.Accolade_Senior, accolade_roster.Accolade_Graduate
			FROM (
				SELECT temp1.First_Name, temp1.Last_Name, temp1.Home_Town, temp1.State_or_Country, temp1.College, temp1.Is_Starter_Freshman, temp1.Is_Starter_Sophomore, temp1.Is_Starter_Junior, temp1.Is_Starter_Senior, temp1.Is_Starter_Senior, temp1.Is_Starter_Graduate, temp1.Height_Freshman, temp1.Height_Sophomore, temp1.Height_Junior, temp1.Height_Senior, temp1.Height_Graduate, weight_roster.Weight_Freshman, weight_roster.Weight_Sophomore, weight_roster.Weight_Junior, weight_roster.Weight_Senior, weight_roster.Weight_Graduate
				FROM (
					SELECT starter_years_roster.First_Name, starter_years_roster.Last_Name, starter_years_roster.Home_Town, starter_years_roster.State_or_Country, starter_years_roster.College, starter_years_roster.Is_Starter_Freshman, starter_years_roster.Is_Starter_Sophomore, starter_years_roster.Is_Starter_Junior, starter_years_roster.Is_Starter_Senior, starter_years_roster.Is_Starter_Senior, starter_years_roster.Is_Starter_Graduate, height_roster.Height_Freshman, height_roster.Height_Sophomore, height_roster.Height_Junior, height_roster.Height_Senior, height_roster.Height_Graduate 
					FROM starter_years_roster 
					JOIN height_roster
					ON starter_years_roster.First_Name=height_roster.First_Name AND starter_years_roster.Last_Name=height_roster.Last_Name AND starter_years_roster.Home_Town=height_roster.Home_Town AND starter_years_roster.State_or_Country=height_roster.State_or_Country AND starter_years_roster.College=height_roster.College
				) AS temp1
				JOIN weight_roster
				ON temp1.First_Name=weight_roster.First_Name AND temp1.Last_Name=weight_roster.Last_Name AND temp1.Home_Town=weight_roster.Home_Town AND temp1.State_or_Country=weight_roster.State_or_Country AND temp1.College=weight_roster.College
			) AS temp2
			JOIN accolade_roster
			ON temp2.First_Name=accolade_roster.First_Name AND temp2.Last_Name=accolade_roster.Last_Name AND temp2.Home_Town=accolade_roster.Home_Town AND temp2.State_or_Country=accolade_roster.State_or_Country AND temp2.College=accolade_roster.College
		) AS temp3
		JOIN starter_count_roster 
		ON temp3.First_Name=starter_count_roster.First_Name AND temp3.Last_Name=starter_count_roster.Last_Name AND temp3.Home_Town=starter_count_roster.Home_Town AND temp3.State_or_Country=starter_count_roster.State_or_Country AND temp3.College=starter_count_roster.College
	) AS temp4
	JOIN bio_link_roster
	ON temp4.First_Name=bio_link_roster.First_Name AND temp4.Last_Name=bio_link_roster.Last_Name AND temp4.Home_Town=bio_link_roster.Home_Town AND temp4.State_or_Country=bio_link_roster.State_or_Country AND temp4.College=bio_link_roster.College
);


#Goal 2, Step 8

DROP TABLE roster_master_data;
DROP TABLE starter_years_roster;
DROP TABLE height_roster;
DROP TABLE weight_roster;
DROP TABLE accolade_roster;
DROP TABLE starter_count_roster;
DROP TABLE bio_link_roster;


