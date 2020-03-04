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
				ON temp1.First_Name=temp2.First_Name, temp1.Last_Name=temp2.Last_Name, temp1.Home_Town=temp2.Home_Town, temp1.State_or_Country=temp2.State_or_Country, temp1.College=temp2.College
			) AS temp2b
			JOIN (
				SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Is_Starter AS Is_Starter_Junior 
				FROM roster_master_data 
				WHERE Year = 'Junior'
			) AS temp3 
			ON temp2b.First_Name=temp3.First_Name, temp2b.Last_Name=temp3.Last_Name, temp2b.Home_Town=temp3.Home_Town, temp2b.State_or_Country=temp3.State_or_Country, temp2b.College=temp3.College
		) AS temp3b 
		JOIN (
			SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Is_Starter AS Is_Starter_Senior 
			FROM roster_master_data 
			WHERE Year = 'Senior'
		) AS temp4 
		ON temp3b.First_Name=temp4.First_Name, temp3b.Last_Name=temp4.Last_Name, temp3b.Home_Town=temp4.Home_Town, temp3b.State_or_Country=temp4.State_or_Country, temp3b.College=temp4.College
	) AS temp4b 
	JOIN (
		SELECT First_Name, Last_Name, Home_Town, State_or_Country, College, Is_Starter AS Is_Starter_Graduate 
		FROM roster_master_data 
		WHERE Year = 'Graduate'
	) AS temp5 
	ON temp4b.First_Name=temp5.First_Name, temp4b.Last_Name=temp5.Last_Name, temp4b.Home_Town=temp5.Home_Town, temp4b.State_or_Country=temp5.State_or_Country, temp4b.College=temp5.College
);
