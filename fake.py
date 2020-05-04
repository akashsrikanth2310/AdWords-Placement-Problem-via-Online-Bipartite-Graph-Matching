# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 23:09:32 2020

@author: Vidhya
"""

import pandas as pd
import sys
import random
import math

random.seed(0)

def calculateRevenue(total_budget,all_bids,	queries,algorithm):
	total_revenue = 0.0
	
	if algorithm == "Greedy":
			revenue = Greedy(dict(total_budget),all_bids,queries)
			
	if algorithm == "MSVV":
			revenue = MSVV(dict(total_budget),all_bids,queries)
			
	if algorithm == "Balance":
			revenue = Balance(dict(total_budget),all_bids,queries)
	
	print("Revenue using "+algorithm+" is : ",revenue)
	
	opt = 0
	for key in total_budget:
		opt+=total_budget[key]
		
	for i in range(100):
		random.shuffle(queries)
		if algorithm == "Greedy":
			revenue = Greedy(dict(total_budget),all_bids,queries)
			
		if algorithm == "MSVV":
			revenue = MSVV(dict(total_budget),all_bids,queries)
			
		if algorithm == "Balance":
			revenue = Balance(dict(total_budget),all_bids,queries)
		total_revenue+=revenue
	return (total_revenue/100)/opt
		


def Greedy(total_budget,all_bids,queries):
	revenue=0.0
	for q in queries:
		temp = all_bids[q]
		max_bid = -1
		bid_by = None
		if checkNeighbours(temp,total_budget)==-1:continue
		for key in temp:
			if  temp[key]<=total_budget[key]:
				if temp[key]>max_bid:
					max_bid=temp[key]
					bid_by = key
				if temp[key]==max_bid:
					bid_by = min(bid_by,key)
					
		revenue+=max_bid
		total_budget[bid_by] = total_budget[bid_by]-max_bid
		
	return revenue
				
		
def MSVV(total_budget,all_bids,queries):
	total = dict(total_budget)
	revenue=0.0
	for q in queries:
		temp = all_bids[q]
		bid_by = next(iter(temp))
		if checkNeighbours(temp,total_budget)==-1:continue
		for key in temp:
		
			if(total_budget[key]>=temp[key]):
			
				x_u_max = (total[bid_by]-total_budget[bid_by])/total[bid_by]
				x_u = (total[key] - total_budget[key])/total[key]
				
				factor1 = 1-math.exp(x_u-1)
				factor2 = 1-math.exp(x_u_max-1)
		
				if factor1*temp[key]>factor2*temp[bid_by]:
					bid_by = key
				if factor1*temp[key]==factor2*temp[bid_by]:
					bid_by = min(bid_by,key)
					
		revenue+=temp[bid_by]
		total_budget[bid_by] = total_budget[bid_by]-temp[bid_by]
		
	return revenue


def Balance(total_budget,all_bids,queries):
	revenue=0.0
	for q in queries:
		temp = all_bids[q]
		maxi = -1
		bid_by = None
		if checkNeighbours(temp,total_budget)==-1:continue
		for key in temp:
			if total_budget[key]>=temp[key]:
				if total_budget[key]>maxi:
					maxi=total_budget[key]
					bid_by = key
				if total_budget[key]==maxi:
					bid_by = min(bid_by,key)
		revenue+=temp[bid_by]
		total_budget[bid_by] = total_budget[bid_by]-temp[bid_by]
		
	return revenue
	
	
def checkNeighbours(temp,total_budget):
	for key in temp:
		if total_budget[key]>=temp[key]:return 0
	return -1
	

	
if len(sys.argv) != 2:
    print('Please enter the preferred algorithm : 1)Greedy 2)MSVV 3)Balance')
    sys.exit(1)
	
algorithm = sys.argv[1]
bidder_data = pd.read_csv("bidder_dataset.csv")

with open('queries.txt') as f:
	queries = f.readlines()
queries = [x.strip() for x in queries]


total_budget = {}
all_bids = {}


for i in range(len(bidder_data)):
	adv_id = bidder_data.iloc[i]['Advertiser']
	keyword = bidder_data.iloc[i]['Keyword']
	bid_value = bidder_data.iloc[i]['Bid Value']
	budget = bidder_data.iloc[i]['Budget']
	
	if adv_id not in total_budget:
		total_budget[adv_id] = budget
		
	if keyword not in all_bids:
		all_bids[keyword] = {}
		
	if adv_id not in all_bids[keyword]:
		all_bids[keyword][adv_id] = bid_value
print(all_bids)
ans = calculateRevenue(total_budget,all_bids,queries,algorithm)
print("Competitve ratio using "+algorithm+" is : ",ans)