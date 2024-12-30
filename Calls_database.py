# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 20:35:28 2020

@author: Andreea
"""

import pandas as pd
import numpy as np
import datetime as dt
import random


def dates_active(start_date, end_date):
    """Generate a list of dates between go live and quit date, if available.

    In case end date does not exist, take the alternative_end, which in our
    case will be the end of the year based on the max(GoLive date).
    """
    dlist = pd.bdate_range(start_date, end_date).to_pydatetime().tolist()
    return dlist


def talk_time(aht):
    """Generate random talk time value.

    Takes in the target aht of the department and returns a float.
    """
    tt_deviation = aht * 0.3
    tt = np.random.normal(loc=aht, scale=tt_deviation)
    return tt


def generate_random_time():
    """Generate random timestamps for the call time.

    The assumption is that there are 2 peaks/day, with an offset of 180 min.
    """
    if random.random() < 0.5:
        time_rand = dt.time(11, 0)
    else:
        time_rand = dt.time(16, 0)

    time_offset = np.random.normal(loc=0, scale=180)
    delta = dt.timedelta(minutes=time_offset)

    # Use a base date safely within the range
    base_date = dt.date(2000, 1, 1)  # Avoid year 1 to prevent overflow

    try:
        final_time = (dt.datetime.combine(base_date, time_rand) + delta).time()
        return final_time.strftime("%H:%M")
    except OverflowError:
        # Handle rare edge case where delta creates an invalid time
        return time_rand.strftime("%H:%M")


def next_time(prev_time, prev_call_time, min_offset, break_time_minutes):
    """Generate timestamps for the call time following the first random time.

    Takes into account the max break time, previous call time and minimum time
    between calls.
    Generates a random time between calls and adds it to the prev. timestamp.
    """
    minutes_to_sec = (break_time_minutes * 60) + (prev_call_time * 60)
    random_offset = random.uniform(min_offset, minutes_to_sec)
    delta = dt.timedelta(seconds=random_offset)
    time_obj = (dt.datetime.strptime(prev_time, "%H:%M")).time()

    final_time = (dt.datetime.combine(
        dt.date(1, 1, 1), time_obj) + delta).time()
    return final_time.strftime("%H:%M")


def answer_time(min_answer, max_answer):
    """Generate random answer time in seconds.

    Takes into account the defied min and max values.
    """
    time_answer = random.randint(min_answer, max_answer)
    return time_answer


def hold_time(min_hold, max_hold):
    """Generate random hold duration in seconds.

    Assumption is that 43% of calls will have hold times between the defied
    min and max values.
    """
    rand_hold = random.randint(min_hold, max_hold)

    if random.random() < 0.43:
        hld_t = rand_hold
    else:
        hld_t = None
    return hld_t


def end_of_year(go_live_series):
    """Generate the end date for the iteration.

    Takes the max go live year and takes the end of that year as dataset end.
    """
    dates_list = pd.Series(go_live_series).dropna()
    max_date = dates_list.max()
    eoy = dt.date((dt.datetime.strptime(max_date, "%Y-%m-%d").date()).year, 12, 31)
    return eoy


# import Userfile, create needed dfs and variables
needed_cols = ["GoLive date", "Leave date",
               "Department", "Job Title", "Norm", "Phone login"]
users = pd.read_csv("Userfile.csv", usecols=needed_cols, parse_dates=True)
agents = users[(users["Job Title"] == "Agent")]
live_dates = users['GoLive date']

# adding all assumptions that need to be taken into account
wt_w_util = {
    # Norm: Worked time w/82% util
    1: 6.56,
    0.75: 4.92,
    0.5: 3.28
}

break_time = {
    # Norm: break time in minutes / 2
    1: 30,
    0.75: 15,
    0.5: 8
}

aht_dept = {
    # Department: AHT Target in minutes
    'Sales': 10,
    'Billing': 8,
    'Technical': 14,
    'Complaints': 23
}

# Columns to be generated & list creation
columns = ["Date", "Time_Received", "Answer time (seconds)",
           "Hold time (seconds)", "Duration (minutes)", "Agent"]

data = []

# Iterate over dataflow using the index attribute - NEED TO SKIP any whose live
# date is nan as that person did not complete the training.

for ind in agents.index:
    norm = agents["Norm"][ind]
    target_wt = wt_w_util[norm] * 60
    max_break_time = break_time[norm]

    department = agents["Department"][ind]
    target_aht = aht_dept[department]

    if pd.isna(agents["GoLive date"][ind]):
        continue  # Skip this iteration if GoLive date is NaN
    else:
        date_start = dt.datetime.strptime(str(agents["GoLive date"][ind]), "%Y-%m-%d").date()

    leave_date = agents["Leave date"][ind]
    if leave_date != leave_date:
        date_end = end_of_year(live_dates)
    else:
        date_end = dt.datetime.strptime(str(agents["Leave date"][ind]),
                                        "%Y-%m-%d").date()
    dates = dates_active(date_start, date_end)

    user = agents["Phone login"][ind]
    first_call = generate_random_time()
    worked_time = 0.0

    for date in dates:
        first_call = generate_random_time()
        time = None
        while worked_time < target_wt:
            answ_time = answer_time(0, 14)
            h_time = hold_time(30, 210)
            duration = talk_time(target_aht)
            worked_time += duration

            if time is None:
                time = first_call
            elif time == first_call:
                time = next_time(first_call, duration, 5, max_break_time)
            else:
                time = next_time(time, duration, 5, max_break_time)
            data.append([date, time, answ_time, h_time, duration, user])

df = pd.DataFrame(data, columns=columns)
df.sort_values(by='Date')
df.to_csv("Calls.csv", encoding='utf-8-sig', index=False)
print("Saved to file")
