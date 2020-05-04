# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 22:46:55 2020

@author: Vidhya
"""
import sys
import pandas as pd
import math
import random
import numpy as np

#findrevenue function prints revenuve and return the total revenue 


def findingExpo(x):      #function to find exponent values
    return math.exp(x)

def findRevenue(length_of_bidder,data_bidders_val_dup,required_algo_val,dictionary_of_budget,dictionary_of_bids,queriesobtained):
    check_val = required_algo_val
    if check_val == "greedy":     #checks greedy algo
        print(GreedyAlgo(length_of_bidder,data_bidders_val_dup,dict(dictionary_of_budget),dictionary_of_bids,queriesobtained))
    elif check_val == "msvv":     #checks msvv algo
        print(MSVVAlgo(length_of_bidder,data_bidders_val_dup,dict(dictionary_of_budget),dictionary_of_bids,queriesobtained))
    elif check_val == "balance":  #checks balance algo
        print(BalanceAlgo(length_of_bidder,data_bidders_val_dup,dict(dictionary_of_budget),dictionary_of_bids,queriesobtained))
        
        
    #calculate the total revenue  
    calculator = 0
    for key, value in dictionary_of_budget.items():
        calculator = calculator + value    #stores the optimal value that is mentioned in project description
    iterator = 1
    revenue_tots = 0.0
    while(iterator < 101):    #runs for 100 iterations as mentioned in the project description
        random.shuffle(queriesobtained)       #using random.shuffle  to shuffle query values
        if check_val == "greedy":     #checks greedy algo
            revenue_tots  = revenue_tots + GreedyAlgo(length_of_bidder,data_bidders_val_dup,dict(dictionary_of_budget),dictionary_of_bids,queriesobtained)
        elif check_val == "msvv":     #checks msvv algo
            revenue_tots  = revenue_tots + MSVVAlgo(length_of_bidder,data_bidders_val_dup,dict(dictionary_of_budget),dictionary_of_bids,queriesobtained)
        elif check_val == "balance":  #checks balance algo
            revenue_tots  = revenue_tots + BalanceAlgo(length_of_bidder,data_bidders_val_dup,dict(dictionary_of_budget),dictionary_of_bids,queriesobtained)
        iterator = iterator + 1     
    divided_by_100 = revenue_tots / 100      #dividing by 100 to get the shuffle values out
    return round(divided_by_100/calculator,2)


#checks for neighbours who can participate in the values 
    

def neighbour_value_return(advid_dict,dictionary_of_budget):
    keys1 = advid_dict.keys()
    keys2 = advid_dict.values()   
    vals1 = dictionary_of_budget.keys()
    for key, value in advid_dict.items():   
        vals2 = dictionary_of_budget[key]  #checking if neighbour values
        if(value <= vals2):     
            return False             #returning false
        else:
            valtoreturn=True         #returning true
    return valtoreturn        

    


        
#Algorithm for greedy 


def GreedyAlgo(length_of_bidder,data_bidders_val_dup,dictionary_of_budget,dictionary_of_bids,queriesobtained):
     revenue_obtained = 0.0
     iterator = 0
     counter = 0
     while(iterator < len(queriesobtained)):    #Looping the queries obtained
         highestbid = -sys.maxsize -1           #setting the minimum value for highest bid
         bidder = None
         counter = counter + 1
         isAbleToProceed = neighbour_value_return(dictionary_of_bids[queriesobtained[iterator]],dictionary_of_budget) #checking if neighbours can proceed
         if(isAbleToProceed):
             counter = counter + 1
             iterator = iterator + 1
             continue;
         else:
             for key,value in dictionary_of_bids[queriesobtained[iterator]].items():   #iterating using .items() [Reference link : https://realpython.com/iterate-through-dictionary-python/]
                 valobtained = dictionary_of_budget[key]   
                 if valobtained >= value:
                     counter = counter + 1
                     highestbid1 = highestbid
                     highestbid = value if highestbid < value else highestbid #choosing highest bid value
                     bidder = key if highestbid1 < value else bidder          #choosing the bidder value
                     if value == highestbid:
                         if bidder > key:
                             bidder = key
                         else:
                              bidder = bidder
             revenue_obtained = revenue_obtained + highestbid      #adding to the revenue obtained vals
             counter = counter + 1
             dictionary_of_budget[bidder] -=  highestbid           #reducing the total budget
             iterator = iterator + 1
     return round(revenue_obtained,2)


#Algorithm for MSVV 


def MSVVAlgo(length_of_bidder,data_bidders_val_dup,dictionary_of_budget,dictionary_of_bids,queriesobtained):
    revenue_obtained = 0.0  #variable for revenue check
    iterator = 0
    counter = 0
    totaldict = dict(dictionary_of_budget)    #converting into dictionary of dictionaries
    while(iterator < len(queriesobtained)):
        highestbid = -sys.maxsize -1   #setting least integer value possible
        iter_val = iter(dictionary_of_bids[queriesobtained[iterator]])  #select new value each time using iterable [Reference link : https://www.programiz.com/python-programming/methods/built-in/iter]
        counter = counter + 1
        bidder = next(iter_val)
        isAbleToProceed = neighbour_value_return(dictionary_of_bids[queriesobtained[iterator]],dictionary_of_budget)  #checks for neighbour values
        if(isAbleToProceed):
            iterator = iterator + 1
            continue;        #continues if not possible
        else:
            for key,value in dictionary_of_bids[queriesobtained[iterator]].items():    #iterating using .items() [Reference link : https://realpython.com/iterate-through-dictionary-python/]
                valobtained = dictionary_of_budget[key]
                if valobtained >= value:
                    subtracted_val = totaldict[bidder]-dictionary_of_budget[bidder]   #subtracting as per despcription 
                    divided_val = subtracted_val/totaldict[bidder]
                    xmax = divided_val-1                                          #finding xmax
                    counter = counter + 1
                    subtracted_val = totaldict[key]-dictionary_of_budget[key]
                    divided_val = subtracted_val/totaldict[key]
                    xu = divided_val-1                                            #finding xu
                    counter = counter + 1
                    
                    exponenent_val1 = findingExpo(xmax)                           #using exponents in calculation
                    exponenent_val2 = findingExpo(xu)
                    
                    factor2= 1-exponenent_val1
                    factor1= 1-exponenent_val2
                    
                    multipled_val1 = value*factor1                                 #multipled vals
                    temporary = dictionary_of_bids[queriesobtained[iterator]]
                    multipled_val2 = factor2*temporary[bidder]                    #multipled vals
                    
                    bidder = key if  multipled_val2 < multipled_val1 else bidder
                    if multipled_val1 == multipled_val2:
                        if bidder > key:
                            bidder = key
                        else:
                             bidder = bidder
            temporary = dictionary_of_bids[queriesobtained[iterator]]
            revenue_obtained = revenue_obtained + temporary[bidder]                   #adding on the revenue vals
            counter = counter + 1
            dictionary_of_budget[bidder] -=  temporary[bidder]
            iterator = iterator + 1
    return round(revenue_obtained,2)      
                         
                    
                    
#Algorithm for Balance                    
                    

def BalanceAlgo(length_of_bidder,data_bidders_val_dup,dictionary_of_budget,dictionary_of_bids,queriesobtained):
    revenue_obtained = 0.0         #calculating revenue details
    iterator = 0
    while(iterator < len(queriesobtained)):
        highestbid = -sys.maxsize -1       #selecting least integer val
        bidder = None
        isAbleToProceed = neighbour_value_return(dictionary_of_bids[queriesobtained[iterator]],dictionary_of_budget) #checking if neighbours can proceed
        if(isAbleToProceed):
            iterator = iterator + 1
            continue;
        else:
            for key,value in dictionary_of_bids[queriesobtained[iterator]].items():  #iterating using .items() [Reference link : https://realpython.com/iterate-through-dictionary-python/]
                valobtained = dictionary_of_budget[key]
                if valobtained >= value:
                    highestbid1 = highestbid
                    highestbid = valobtained if highestbid < valobtained else highestbid
                    bidder = key if highestbid1 < valobtained else bidder
                    if valobtained == highestbid:
                        if bidder > key:
                            bidder = key
                        else:
                             bidder = bidder
            temporary = dictionary_of_bids[queriesobtained[iterator]]        
            revenue_obtained = revenue_obtained + temporary[bidder]    #adding onto the revenue details
            dictionary_of_budget[bidder] -=  temporary[bidder] 
            iterator = iterator + 1
    return round(revenue_obtained,2)
     
    
         
def formZip(data_bidders_val):
    return zip(data_bidders_val.Advertiser,data_bidders_val.Budget)

def findrowvals(data_bidders_val,iterator):
 rowvals = []
 rowvals.append(data_bidders_val.iloc[iterator]['Advertiser'])
 rowvals.append(data_bidders_val.iloc[iterator]['Keyword'])
 rowvals.append(data_bidders_val.iloc[iterator]['Bid Value'])
 return rowvals
 
def findQueries(filename):
    with open(filename, 'r') as quer:
        queriesobtained = [q.strip() for q in quer]
    return queriesobtained
    

#setting seed as 0

random.seed(0)

#selecting the required algorithm via the command line

length_of_arguments = len(sys.argv)
if(length_of_arguments < 2):
    print('the command line input for the algorithm is not entered, please enter i)greedy ii)msvv iii)balance')
    sys.exit(1)

if(sys.argv[1] == 'msvv' or sys.argv[1] == 'greedy' or sys.argv[1] == 'balance' ):
    required_algo_val = sys.argv[1]
    #reading the bidder data set
    data_bidders_val = pd.read_csv("bidder_dataset.csv")
    #reading in the queries
    filename = "queries.txt"
    queriesobtained = findQueries(filename)     #function findQueries is called
    #creating a dictionary for budget and advertiser
    data_bidders_val_dup = data_bidders_val.dropna()      #Droping the duplicate values of the rows
    forming_zip = formZip(data_bidders_val_dup)           #using the zip structure to get vals
    dictionary_of_budget = dict(forming_zip)              #forming a dictionary
    
    #calculating length of the bidder csv 
    length_of_bidder = len(data_bidders_val)
    iterator = 0
    dictionary_of_bids = {}               #hold the dictionary details for bids
    while(iterator < length_of_bidder):   #loops through the entire bidder dataset
        count1 = 1 
        count2 = 1
        listofvals = findrowvals(data_bidders_val,iterator)  #returns the value at the specified positions
        if listofvals[1] in dictionary_of_bids:
            count1 = count1 + 1 
        else:
            dictionary_of_bids[listofvals[1]] = {}           #creates values as dictionary
        if listofvals[0] in dictionary_of_bids[listofvals[1]]:
            count2 = count2 + 1
        else:
            dictionary_of_bids[listofvals[1]][listofvals[0]] = listofvals[2]   #sets the bid value at the right position 
        iterator = iterator + 1    
    
    print(findRevenue(length_of_bidder,data_bidders_val_dup,required_algo_val,dictionary_of_budget,dictionary_of_bids,queriesobtained))    
else:
    print('the command line input for the algorithm should be entered as, please enter i)greedy ii)msvv iii)balance')
    sys.exit(1)
    
