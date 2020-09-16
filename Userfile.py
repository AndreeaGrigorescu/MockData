# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 08:04:15 2020.

@author: Andreea
"""

import pandas as pd
from random import randint

hr_file = pd.read_csv("HR Database.csv").drop(["Education", "DoB"], axis=1)

user_file = hr_file.convert_dtypes()
user_file["Hire date"] = user_file["Hire date"].astype('datetime64').dt.date
user_file["Leave date"] = pd.to_datetime(user_file["Leave date"]).dt.date

user_list = []
department = user_file["Department"]
f_name = user_file["First Name"]
l_name = user_file["Last Name"]


for i in range(len(user_file)):
    username = (department[i][:1] + str(randint(0, 99)) +
                f_name[i][:3] +
                l_name[i][:4]).lower()
    user_list.append(username)

user_file["Username"] = user_list
user_file["Phone login"] = 782123 + hr_file["Employee_ID"]

user_file.to_csv("Userfile.csv", encoding='utf-8-sig', index=False)
