# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:27:31 2019

@author: Diego
"""

import datetime

def list_of_daily_dates(time):
    
    last_time = time[-1]
    if last_time>=1:
        n_day_years = last_time*365
        n_excess_day = (last_time - int(last_time))*365
        n_day_from_today = int(round(n_day_years+n_excess_day,0))
    
    else :
        n_day_from_today = int(round(last_time*365,0))
        
    
    dates=[]
    dates.append(datetime.date.today())
    
    for i in  range(0, n_day_from_today):
        
        next_day_date = dates[i]+datetime.timedelta(days=1)
        dates.append(next_day_date)
    
    
    annual_basis_date =[]
    annual_basis_date.append(1/365)
    for i in  range(0, n_day_from_today-1):
        
        next_annual_basis_date = annual_basis_date[i]+1/365
        annual_basis_date.append(next_annual_basis_date)
    
    
    
    return dates, annual_basis_date


#time = [0 , 0.00821917808219178]

#dates, annual_basis_date = list_of_daily_dates(time)


    
    
    
