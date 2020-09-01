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
  	a. First Name
		b. Last Name
		c. Employee_ID
		d. Hire date
		e. Date of Birth (DoB)
		f. Education
		g. Position - renamed to Job Title
		h. Norm
    i. Department
 
# Source:
  
  Inspiration for the project and specific code elements was given by Keith Galli:
  
    https://www.youtube.com/watch?v=VJBY2eVtf7o&t=2589s
    https://github.com/KeithGalli/Pandas-Data-Science-Tasks/tree/master/Misc
    
  First and Last Name was retrieved from Wikipedia using Power BI to do a basic data cleanup prior to saving the information as *.csv. 
  
    First names: https://en.wikipedia.org/wiki/List_of_most_popular_given_names
    Surnames: https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_Europe
   
