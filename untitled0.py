#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 17:01:49 2018

@author: kacper
"""

def max_profit(arr):
    profit = 0
    idx = 0
    indicies = [0, 0]
    
    for i in range(1, len(arr)):
        
        if(profit < arr[i] - arr[idx]):
            profit = arr[i] - arr[idx]
            indices = [idx, i]
            
        if(arr[i] < arr[idx]):
            idx = i
            
    arr.pop(indices[1])
    arr.pop(indices[0])
    return profit, arr
    
def total_profit(k, arr):
    total_profit = 0
    
    for _ in range(k):
        p, arr = max_profit(arr)
        total_profit += p
        
    return total_profit

print(total_profit(2, [10, 30, 5, 45, 23, 1000, 3, 100]))