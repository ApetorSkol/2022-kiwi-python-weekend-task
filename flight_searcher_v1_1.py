#!/usr/bin/python

# Kiwi Python weekend entry task
# Author: Matej Slivka
# March 2022

# # # # # # # # # # # # # # # # # # # # 
# This project looks for flights from place A -> B and then sorts them by their price
# This project works with data formated as
# flight_no,origin,destination,departure,arrival,base_price,bag_price,bags_allowed 
#
# Usage:
# python3 flight_searcher.py [flights] [origin] [destination]
# Where 
# flights     : is an input folder with flights
# origin      : is origin of route
# destination : is destination of route
# # # # # # # # # # # # # # # # # # # # 



import argparse                 # for working with arguments
import csv                      # for working with csv
import datetime                 # for working with date
import json
from textwrap import indent     # for working with output

one_hour= datetime.timedelta(hours=1)
two_hours = datetime.timedelta(hours=2)
three_hour= datetime.timedelta(hours=3)
four_hours = datetime.timedelta(hours=4)
five_hour= datetime.timedelta(hours=5)
six_hours = datetime.timedelta(hours=6)
seven_hour= datetime.timedelta(hours=7)
eight_hours = datetime.timedelta(hours=8)
nine_hour= datetime.timedelta(hours=9)
ten_hours = datetime.timedelta(hours=10)
eleven_hour= datetime.timedelta(hours=11)
twelve_hours = datetime.timedelta(hours=12)

# check wheter x is not part of function
def is_not_reference_to(arr,elem,flights):
    for i in arr:
        if ((flights[i]['destination']  == elem )|(flights[i]['origin'] == elem)):
            return False
    return True

# returns last number
def return_last_num(arr):
    for i in arr[::-1]:
        if i != '|':
            return i    

# check for correct arguments
aparser = argparse.ArgumentParser(description="Program looks for cheapest flights")
aparser.add_help=True
aparser.add_argument('flights', type=str, help="source file with flights")
aparser.add_argument('origin', type=str, help="orgign of our flight") 
aparser.add_argument('destination', type=str, help="destination of our flight") 
aparser.add_argument('--bags', nargs=1 ,required=False ,default=['0'], help="number of bags allowed")
aparser.add_argument('--return',nargs='?',required=False ,default=False, help="True/False depending whether the flights is return flight")
args = aparser.parse_args()
bags_num = "".join(args.bags)


# open folder with flights 
open_file = open(args.flights, "r")
reader = csv.reader(open_file)
# flights stores all flights
# output_flights contains lists of paths that should lead to final destination
# curr_path is current path
output_flights=[]
flights=[]  
todo_stack=[]
curr_path=[]
curr_flight_index = 1

# open file as dictionary
my_dict = csv.DictReader(open_file)
flights = list(my_dict)

# sort flights by their departure time
flights.sort(key=lambda x: x['departure'])


# get all cities with origin
# save direct flights
flights_order = 0
for row in flights:
    if (row['origin'] == args.origin)&(int(row['bags_allowed']) >= int(bags_num)):
        if row['destination'] == args.destination:
            output_flights.append([flights_order])
        else:
            todo_stack.append(flights_order)
    flights_order+=1

# chceck whether we have any origin cities
# '|' is a symbol which I push to todo_stack. It is symbol which signals that we have checked all nodes on one
if todo_stack:
    curr_path.append(todo_stack[-1])
    todo_stack.append('|')
else:
    exit


#constants for work later
one_hour= datetime.timedelta(hours=1)
six_hours = datetime.timedelta(hours=6)
# recursive looking while stack is not empty
while todo_stack:
    curr_flight_index = int(curr_path[-1])
    current_flight = flights[curr_flight_index]
    arrival_time_plus_one = datetime.datetime.fromisoformat(current_flight['arrival'])+one_hour
    arrival_time_plus_six = datetime.datetime.fromisoformat(current_flight['arrival'])+six_hours
    i = 1
    # check every child of given parent
    while (curr_flight_index + i < flights_order):
        incoming_flight_order = curr_flight_index + i
        incoming_flight = flights[incoming_flight_order]
        incoming_flight_time = datetime.datetime.fromisoformat(incoming_flight['departure'])
        # check for correct time and number of bags
        if  incoming_flight_time > arrival_time_plus_six:
            break
        if (incoming_flight_time < arrival_time_plus_one) | (int(incoming_flight['bags_allowed']) < int(bags_num)):
            i+=1
            continue
        # check wheter we are hitting destination
        if ((incoming_flight['destination'] == args.destination) & (current_flight['destination'] == incoming_flight['origin'] )):
            curr_path.append(incoming_flight_order)
            output_flights.append(curr_path.copy())
            curr_path.pop()
        # check if flight is part of path
        elif ((incoming_flight['origin'] == current_flight['destination']) & is_not_reference_to(curr_path,incoming_flight['destination'],flights)):
            todo_stack.append(incoming_flight_order)

        i+=1

    # if we have checked all children or if the path has not changed
    # then pop todo_stack and change curr path
    if ((todo_stack[-1]=='|') | ((return_last_num(todo_stack)) == curr_path[-1])):
        while (todo_stack[-1] =='|'):
            todo_stack.pop()
            todo_stack.pop()
            curr_path.pop()
            # break if we did all work
            if not todo_stack:
                break
        if todo_stack:
            # signal start of new generation
            curr_path.append(todo_stack[-1])
            todo_stack.append('|')
    else:
        curr_path.append(todo_stack[-1])
        todo_stack.append('|')

# insert price into flights 

for path in output_flights:
    total_price = 0
    for i in path:
        total_price = total_price + float(flights[i]['base_price']) +  float(bags_num[0])*float(flights[i]['bag_price'])
    path.insert(0,total_price)
# sort by price
output_flights.sort(key=lambda x: x[0])

# convert each data to json
output_list = []
flight_list = []
for path in output_flights:
    bags_allowed = flights[path[1]]['bags_allowed']
    for i in path:
        if type(i) == float:
            continue
        bags_allowed= min(bags_allowed, flights[i]['bags_allowed'])
        flight_list.append(
            {
                "flight_no": flights[i]['flight_no'],
                "origin": flights[i]['origin'],
                "destination": flights[i]['destination'],
                "departure": flights[i]['departure'],
                "arrival": flights[i]['arrival'],
                "base_price": float(flights[i]['base_price']),
                "bag_price": float(flights[i]['bag_price']),
                "bags_allowed": int(flights[i]['bags_allowed'])
            })
    output_list.append({
        "flights": 
            flight_list,
        "bags_allowed": int(bags_allowed),
        "bags_count": int(bags_num[0]),
        "destination": args.destination,
        "origin": args.origin,
        "total_price": float(path[0]),
        "travel_time": str(datetime.datetime.fromisoformat(flights[path[-1]]['arrival']) - datetime.datetime.fromisoformat(flights[path[1]]['departure'])) 
    })
    flight_list=[]

# print output
print(json.dumps(output_list, indent=4)) 
# close file we worked with
open_file.close()



#This ninja ensures proper functionality of project, keep him at all costs!
#                 ////////                 MMM
#            //////////////////           MMM
#          /////////////////////        MMM
#         ///////////////////////      MMM
#        /////////////////////////    MM
#         /////////////////////////  M
#        //////////////////////////   
#        /////////////////////////   
#                   /    ////////   /
#           $$    $$$       ////   //
#                           ///   ///
#                         ////   ///
#         ////     //////////   ////
#          /////////////////   ////
#           ///////////////   ////
#            /////////////   ////
#              ///////        //
#                 ///     |    ///
#               /////    |     /////
#             ////////        //////
#            ///////   ///////////
#           ////        ////////
#          ///    |      /////
#           ///  |      //////
#          /////      /////////
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   
