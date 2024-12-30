# MockData
Generates mock customer service data for further analysis and visualisations building.

Finding data that respects real life business rules and is free to use is hard to find. 
This project was created to solve this problem by generating mock data that encompasses the realities of the call center/customer care industry.

# 1. HR Data

Assumptions implemented:
  5000 employees in total, out of which a maximum of 10% support staff;  
  A maximum of 9% staff turnover with a random number of days worked;  
  All support staff works full time;  
  All support staff has higher education (Undergraduate or Graduate);  
  Employee IDs are unique and corelated with the Hire date.  
  
Columns included:  
  	+ First Name \
	* Last Name \
	- Employee_ID \
	* Hire date \
	+ Date of Birth (DoB) \
	* Education \
	- Position - renamed to Job Title \
	* Norm \
    	+ Department 

# 2. User file

Based on the HR Dataset with the following adjustments:
	a. Removed the education and Date of Birth columns.
	b. Added UserName column - unique values.
	c. Added Phone login - unique values


# 3 Calls database

Contains the following columns:
	a. Date
	b. Time_Received
	c. Answer time (seconds)
	d. Hold time (seconds)
	e. Duration (minutes)
	f. Agent

Assumptions that were implemented:
	1. Agent utilization of 82%
	2. Norm specific daily break durations
	3. Specific department AHT

For each agent establishes the timeframe worked: either leave date or the end of the year of the maximum GoLive dates.
Iterates through each day and each agent to generates calls with random hold and answer times, both as per a specifically set interval as well as the calls until we reach maximum utilization for that specific agent.

# Source:
  
  Inspiration for the project and specific code elements was given by Keith Galli:
  
    https://www.youtube.com/watch?v=VJBY2eVtf7o&t=2589s
    https://github.com/KeithGalli/Pandas-Data-Science-Tasks/tree/master/Misc
    
  First and Last Name was retrieved from Wikipedia using Power BI to do a basic data cleanup prior to saving the information as *.csv. 
  
    First names: https://en.wikipedia.org/wiki/List_of_most_popular_given_names
    Surnames: https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_Europe
   
