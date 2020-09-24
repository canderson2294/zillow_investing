#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 14:23:44 2020

@author: camille
"""

import pandas as pd
metro =  pd.read_csv('Metro.csv')
metro = metro[['RegionID', 'RegionName', 'SizeRank', '2019-01', '2020-01']]
metro['year_dif'] = metro['2020-01'] - metro['2019-01']


def loadInvestments(file):
    '''Given a file of investments and estimated returns, returns a list of 
    investment options (name, cost, and estimated return).'''
    df = pd.read_csv(file)
    df = df[['RegionID', 'RegionName', 'SizeRank', '2019-01', '2020-01']]
    #calculate the Return on Investment for each region
    # ROI = (return - investment) / investment
    df['ROI'] = (df['2020-01'] - df['2019-01']) / df['2019-01']
    # calculate the estimated return using the Jan. 2020 value as the cost
    df['est_return'] = round((df['2020-01'] * df['ROI']) + df['2020-01'])
    #output investment options with name, cost and estimated return for each
    output = []
    for index, row in df.iterrows():
        name = row['RegionName']
        cost = row['2020-01']
        est_return = row['est_return']
        output.append([name, cost, est_return])
    return output


options = loadInvestments('Metro.csv')    

def optimizeInvestments(options_list, funds, increment):
    '''Given a list of possible investments, the amount of money available
    to spend and the smallest that we increment our funds. Returns the optimal 
    return on investment and the investments selected to produce it.'''
    n = len(options_list)
    #sort the list of investments by ascending cost
    investments = sorted(options_list, key= lambda x: x[1])
    names = [x[0] for x in investments]
    costs = [x[1] for x in investments]
    values = [x[2] for x in investments]
    #the columns of the tables will be 0 to our entire fund, by our provided increment
    invest_fund = [x for x in range(0, funds + increment, increment)]
    #set up table for optimal returns
    optimal = [[None for x in invest_fund] for x in range(n + 1)] 
    #set up traceback table
    tb = [[None for x in invest_fund] for x in range(n + 1)]
    
    #for each possible investment, i
    for i in range(n + 1): 
        #for each increment of our investment fund, f
        for f in range(len(invest_fund)):
            f_val = invest_fund[f]
            #base case: no investment, or $0
            if i == 0 or f == 0: 
                optimal[i][f] = 0
                
            #if the cost of the investment is less than the amount we have to
            #spend (if we can afford to buy)
            elif costs[i-1] <= f_val: 
                #if we buy, the value will be the return on the investment plus 
                #the return we can get with the remainder of our fund
                prev_buy = (f_val - costs[i-1])//increment
                buy = values[i-1] + optimal[i-1][prev_buy]
                #if we don't buy, the value is the return without the current
                dont_buy = optimal[i-1][f]
                #if buying is more profitable, insert the return into the optimal
                #table, and insert the investment info into the traceback
                
                if buy > dont_buy:
                    optimal[i][f] = buy
                    tb[i][f] = [names[i-1], costs[i-1], values[i-1]]
                    
                #else, fill the tables with the information of the more 
                #profitable choice
                else:
                    optimal[i][f] = dont_buy
                    tb[i][f] = tb[i-1][f]
                    
            #if we do not have enough to purchase the investment       
            else: 
                optimal[i][f] = optimal[i-1][f] 
                tb[i][f] = tb[i-1][f]
    
    #last column of the tables                           
    f_index = funds // increment
    a = f_index
    #store the best investments
    best = []
    while a > 0 and n >0:
        current_invest = tb[n][a]
        if current_invest != None:
            inv_cost = current_invest[1]
            best += [current_invest]
            a = a - (inv_cost // increment)
        else:
            n = n-1
            
    invest_return = optimal[len(options_list)][f_index]
    ROI = (invest_return - funds) / funds
    ROI = "{:.2%}".format(ROI)
    print('''
          Given $%d to invest, a return of $%d can be achieved, 
          giving us a profit of $%d and ROI of %s ''' % 
    (funds, invest_return, invest_return - funds, ROI))   
    print('''\nThe following investments produce this return:''')  
    for b in best:
        print('\n')
        print('Location: ' + b[0]) 
        print('Cost: $'+ str(b[1])) 
        print('Estimated Return: $'+ str(b[2])) 
        profit = b[2] - b[1]
        print('Profit: $' + str(profit)) 
        
    return invest_return



optimizeInvestments(options, 1000000, 1000)
