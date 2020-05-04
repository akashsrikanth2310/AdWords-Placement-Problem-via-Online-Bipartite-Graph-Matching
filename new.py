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

ans = calculateRevenue(total_budget,all_bids,queries,algorithm)
print("Competitve ratio using "+algorithm+" is : ",ans)


[213, 287, 205, 197, 287, 108, 312, 44, 152, 138, 301, 285, 175, 158, 170, 37, 158, 158, 152, 37, 126, 301, 138, 108, 137, 256, 169, 287, 184, 287, 32, 170, 32, 64, 37, 152, 158, 323, 126, 128, 267, 205, 126, 67, 312, 205, 83, 301, 312, 161, 323, 138, 158, 268, 126, 32, 126, 292, 211, 152, 272, 205, 199, 197, 205, 287, 152, 108, 205, 205, 256, 216, 37, 205, 285, 99, 137, 83, 99, 126, 272, 37, 272, 83, 211, 272, 126, 268, 287, 211, 86, 161, 216, 170, 181, 184, 158, 167, 292, 175, 268, 138, 170, 99, 44, 201, 158, 152, 175, 83, 158, 170, 60, 323, 169, 211, 170, 285, 128, 108, 158, 83, 83, 37, 86, 323, 323, 312, 128, 167, 197, 137, 175, 83, 256, 259, 44, 32, 138, 60, 86, 230, 268, 175, 184, 128, 167, 158, 60, 272, 83, 205, 67, 323, 268, 323, 216, 201, 158, 37, 312, 161, 285, 169, 245, 44, 256, 289, 292, 158, 272, 321, 170, 161, 161, 216, 99, 292, 152, 197, 205, 167, 152, 60, 216, 230, 301, 199, 99, 44, 213, 211, 230, 44, 323, 216, 44, 272, 230, 64, 205, 285, 181, 64, 268, 268, 201, 169, 161, 205, 44, 32, 99, 289, 289, 169, 175, 167, 64, 256, 197, 292, 230, 64, 184, 167, 99, 259, 126, 181, 199, 86, 108, 213, 267, 323, 161, 292, 211, 169, 272, 128, 323, 126, 37, 287, 128, 128, 161, 216, 205, 259, 267, 256, 128, 128, 161, 128, 216, 301, 289, 199, 272, 167, 169, 161, 267, 83, 268, 211, 287, 321, 170, 197, 268, 60, 67, 167, 287, 128, 137, 285, 213, 211, 268, 170, 216, 245, 128, 213, 285, 128, 158, 181, 211, 175, 287, 64, 126, 216, 108, 259, 175, 108, 287, 272, 83, 230, 64, 301, 268, 161, 216, 184, 287, 323, 44, 181, 170, 197, 37, 211, 272, 323]