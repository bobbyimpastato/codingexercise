import os
import json
import time
#assume data file is in same repo
import json
from datetime import datetime

#name of file (edit if necessary)
filename = "trainings (correct).txt"

#Load JSON
try:
    myfile = open(filename, 'r')
    data = json.load(myfile)
    print("Opened file")
except:
    print("ERROR OPENING FILE! (Program assumes file is in same repository and named 'trainings (correct).txt'")


#print data
time.sleep(1)
print(json.dumps(data, indent=4))


completed_counts = {}  #store counts

#we iterate through each item (person) in the data
for person in data:
    #dict to store trainings
    recent_trainings = {}

    #iterate through each of their completions
    for completion in person["completions"]:
        training_name = completion["name"]
        timestamp = completion["timestamp"]

        #parse timestamp
        completion_date = datetime.strptime(timestamp, "%m/%d/%Y")

        #only the most recent completion should be considered
        if training_name not in recent_trainings or recent_trainings[training_name] < completion_date:
            recent_trainings[training_name] = completion_date

    #update completed counts dictionary with their recent trainings (create new entty as zero if does not exist)
    for training_name in recent_trainings:
        if training_name not in completed_counts:
            completed_counts[training_name] = 0
        completed_counts[training_name] += 1

#print completed counts
print("\nNumber of people who completed each training:\n")
for name in completed_counts:
    formatted_name = format(name, ">40s")
    print("\t", formatted_name, completed_counts[name],"\n")
