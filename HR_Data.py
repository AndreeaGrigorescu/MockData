# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:31:34 2020.

@author: Andreea
"""

import pandas as pd
import numpy
import datetime
import random


def random_firstName():
    """Retrieve random name from the file and populate 'First Name' column."""
    csvfile = pd.read_csv("Firstnames.csv", usecols=["Name"], squeeze=True)
    return csvfile.sample().item()


def random_lastName():
    """Retrieve random name from the file and populate 'Last Name' column."""
    csvfile = pd.read_csv("Surnames.csv", usecols=["Surname"], squeeze=True)
    return csvfile.sample().item()


def random_dates(year_start, month_start, day_start,
                 year_end, month_end, day_end):
    """Generate random date within interval as per user input."""
    start_date = datetime.datetime(year_start, month_start, day_start,
                                   hour=11, minute=0, second=0, microsecond=0)
    end_date = datetime.datetime(year_end, month_end, day_end,
                                 hour=16, minute=30, second=0, microsecond=0)
    days_between_dates = (end_date - start_date).days
    random_no_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_no_of_days)

    time_offset = numpy.random.normal(loc=0, scale=999999)
    final_date = random_date + datetime.timedelta(microseconds=time_offset)
    return final_date


def leave_date(hire_date, max_date):
    """Generate attrition data.

    Generate employee quit date based on:
    - attrition of around 9%;
    - hire date;
    - random days worked.
    """
    max_int_days = max_date - hire_date.date()
    rand_days_worked = random.randint(0, max_int_days.days)

    if random.random() < 0.09:
        last_day = hire_date + datetime.timedelta(days=rand_days_worked)
    else:
        last_day = None
    return last_day


positions = {
    # Position name: Weight
    'Agent': 60,
    'Team Leader': 2,
    'Quality Specialist': 2,
    'Analyst': 1,
    'Manager': 1
    }

position_list = [position for position in positions]
pos_weight = [positions[position] for position in positions]


columns = ["First Name", "Last Name", "Hire date", "Job Title", "DoB",
           "Education", "Department", "Norm", "Leave date"]

df = pd.DataFrame(columns=columns)

dates_arguments = {
    'Hire': {
        'year start': 2017,
        'month start': 8,
        'day start': 1,
        'year end': 2020,
        'month end': 12,
        'day end': 30
        },
    'Birth': {
        'year start': 1964,
        'month start': 1,
        'day start': 13,
        'year end': 2000,
        'month end': 12,
        'day end': 31
        }
    }
departments = {
        # Department: Weight
        'Sales': 6,
        'Billing': 10,
        'Technical': 7,
        'Complaints': 3
        }

department_list = [department for department in departments]
dep_weight = [departments[department] for department in departments]

norms = {
    # Norm: Weight
    1: 10,
    0.75: 4,
    0.5: 6
    }

norm_list = [norm for norm in norms]
norm_weight = [norms[norm] for norm in norms]

for i in range(5000):
    first_name = random_firstName()
    last_name = random_lastName()

    position_choice = random.choices(position_list, weights=pos_weight)[0]
    department_choice = random.choices(department_list, weights=dep_weight)[0]

    hire_date = random_dates(dates_arguments['Hire']['year start'],
                             dates_arguments['Hire']['month start'],
                             dates_arguments['Hire']['day start'],
                             dates_arguments['Hire']['year end'],
                             dates_arguments['Hire']['month end'],
                             dates_arguments['Hire']['day end']
                             )
    date_of_birth = random_dates(dates_arguments['Birth']['year start'],
                                 dates_arguments['Birth']['month start'],
                                 dates_arguments['Birth']['day start'],
                                 dates_arguments['Birth']['year end'],
                                 dates_arguments['Birth']['month end'],
                                 dates_arguments['Birth']['day end']
                                 )

    date_left = leave_date(hire_date,
                           datetime.date(dates_arguments['Hire']['year end'],
                                         dates_arguments['Hire']['month end'],
                                         dates_arguments['Hire']['day end'])
                           )

    if position_choice == 'Agent':
        education_lvl = random.choice(["High School", "Undergraduate"])
        working_norm = random.choices(norm_list, weights=norm_weight)[0]
    else:
        education_lvl = random.choice(["Undergraduate", "Graduate"])
        working_norm = 1

    df.loc[i] = [first_name, last_name, hire_date,
                 position_choice, date_of_birth.date(), education_lvl,
                 department_choice, working_norm, date_left
                 ]

emp_id = df['Hire date'].rank(method='dense').sub(1).astype(int)
df['Employee_ID'] = emp_id + 1000

df.to_csv("HR Database.csv", encoding='utf-8-sig', index=False)
