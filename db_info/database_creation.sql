#Database Creation



#Goal 1, Step 1

CREATE TABLE roster_data (roster_data.Roster_Year INT, roster_data.Player_Number INT, roster_data.First_Name VARCHAR(50), roster_data.Last_Name VARCHAR(50),  roster_data.Year VARCHAR(10), roster_data.Position1 VARCHAR(10), roster_data.Position2 VARCHAR(10), roster_data.Position3 VARCHAR(10), roster_data.Height VARCHAR(10), roster_data.Weight INT, roster_data.Home_Town VARCHAR(30), roster_data.State_or_Country VARCHAR(20), roster_data.High_School VARCHAR(50), roster_data.Alternative_School VARCHAR(50), roster_data.College VARCHAR(50), roster_data.College_League VARCHAR(20), roster_data.Bio_Link VARCHAR(60));

CREATE TABLE starter_data(starter_data.Roster_Year INT, starter_data.Number INT, starter_data.First_Name VARCHAR(50), starter_data.Last_Name VARCHAR(50), starter_data.Potential_Starts INT, starter_data.GP INT, starter_data.GS INT,starter_data.Is_Starter VARCHAR(1), starter_data.College VARCHAR(50));

# \COPY roster_data FROM 'roster_data.csv' DELIMITER ',' CSV HEADER;

# \COPY starter_data FROM 'starter_data.csv' DELIMITER ',' CSV HEADER;


#Goal 1, Step 2

CREATE TABLE accolade_data(accolade_data.Roster_Year INT, accolade_data.First_Name VARCHAR(50), accolade_data.Last_Name VARCHAR(50), accolade_data.Accolade VARCHAR(20), accolade_data.College VARCHAR(50));

# \COPY accolade_data FROM 'accolades.csv' DELIMITER ',' CSV HEADER;
