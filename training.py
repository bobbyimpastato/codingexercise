import os
import json
import time
#assume data file is in same repo
import json
from datetime import datetime, timedelta  # Ensure timedelta is imported

trainings_input = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]

fiscal_year_input = 2024

target_date = datetime(2023, 10, 1)

day = 1
month = 10
year = 2024

print("Welcome to training.py")
print("Created by Robert (Bobby) Impastato on 9/27/2024 for University of Illinois Urbana-Champaign code screening")


while True:
    print("\nDefault fiscal year:", fiscal_year_input)
    choice = input("Would you like to use default fiscal year? [Y/N]: ")
    if choice == "N" or choice == "n":
        try:
            fiscal_year_input = int(input("Custom Fiscal year: "))
        except:
            print("ERROR: Please enter a number")
        break
    elif choice == "Y" or choice == "y":
        break
    else:
        print("ERROR: Enter Y or N")

while True:
    print("\nDefault trainings parameters:", trainings_input)
    choice = input("Would you like to use default training parameters? [Y/N]: ")
    if choice == "N" or choice == "n":
        newlist = []
        try:

            num_parameters = int(input("How many training parameters?: "))
        except:
            print("ERROR: Please enter a number")
            continue

        for i in range(0,num_parameters):
            parameter = input(f"Parameter {i+1}: ")
            newlist.append(parameter)
        print("New parameters:", newlist)
        trainings_input = newlist

        break
       
    elif choice == "Y" or choice == "y":
        break
    else:
        print("ERROR: Enter Y or N")

while True:
    print("\nDefault expiration date:", target_date)
    choice = input("Would you like to use default expiration date? [Y/N]: ")
    if choice == "N" or choice == "n":
        try:
            day = int(input("Custom expiration day (DD): "))
        except:
            print("ERROR: Please enter a number")
            continue
        try:
            month = int(input("Custom expiration month (MM): "))
        except:
            print("ERROR: Please enter a number")
            continue
        try:
            year = int(input("Custom expiration year (YYYY): "))
        except:
            print("ERROR: Please enter a number")
            continue
        break
    elif choice == "Y" or choice == "y":
        break
    else:
        print("ERROR: Enter Y or N")


#name of file (edit if necessary)
filename = "trainings (correct).txt"

#Load JSON
try:
    myfile = open(filename, 'r')
    data = json.load(myfile)
    print(f"Opened file {filename}")
except:
    print("ERROR OPENING FILE! (Program assumes file is in same repository and named 'trainings (correct).txt'")


#print data
#time.sleep(1)
#print(json.dumps(data, indent=4))


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
    print("\t" + name + ": " + str(completed_counts[name]),"\n")


fiscal_year_start = datetime(fiscal_year_input - 1, 7, 1) #7/1/23
fiscal_year_end = datetime(fiscal_year_input, 6, 30) #6/30/24

#init empty dictionary
people_completetrainings = {}

#iterate through all relevant trainings and add entry to dict
for training in trainings_input:
    people_completetrainings[training] = []

#once again iterate through each item (person) in the data
for person in data:
    for completion in person["completions"]:
        training_name = completion["name"]
        timestamp = completion["timestamp"]
        completion_date = datetime.strptime(timestamp, "%m/%d/%Y")
        
        #check if current training matches target list
        if training_name in trainings_input:
            #check if within target fiscal year
            if fiscal_year_start <= completion_date <= fiscal_year_end:
                people_completetrainings[training_name].append(person["name"])
#print results
print("\nSpecified trainings:",end="")
for item in trainings_input:
    print(item + ", ", end="")
print(f"\nPeople who completed specified trainings in FY {fiscal_year_input}:\n")

for training, people in people_completetrainings.items():
    print(f"{training}:")
    if people:  #check if empty
        for person in people:
            print(f"      {person}")
    else:
        print("      No one completed this training.")  #nobody completed
    
    print("")

target_date = datetime(year, month, day)
one_month_from_target = target_date + timedelta(days=30)

#initialize dict for results
expired_or_expiringsoon = {}

#once again iterate through each item (person) in the data
for person in data:
    person_name = person["name"]
    
    for completion in person["completions"]:
        training_name = completion["name"]
        expiration_date = completion.get("expires")
        
        if expiration_date:  #if expiration date exists, parse
            expiration_date_parsed = datetime.strptime(expiration_date, "%m/%d/%Y")
            
            #check if training or expired (or will soon)

            if expiration_date_parsed < target_date:  #training is expired
                status = "Expired"

            elif expiration_date_parsed <= one_month_from_target:  #training expires soon
                status = "Expires Soon"
            else:
                continue  #skip if neither is true

            #add to dict if doesnt exist yet
            if person_name not in expired_or_expiringsoon:
                expired_or_expiringsoon[person_name] = []
            
            expired_or_expiringsoon[person_name].append({
                "training": training_name,
                "status": status
            })

#print result
print(f"\nPeople with trainings that are expired or expiring soon ({target_date}):\n")
for person, trainings in expired_or_expiringsoon.items():
    print(f"{person}:")
    for training_info in trainings:
        print(f"      {training_info['training']} ({training_info['status']})")
