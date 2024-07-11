# -*- coding: utf-8 -*-

#Importing dependencies
import pandas as pd
import numpy as np
import re


def preprocessing(data):
    #Extracting messages
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern,data)[1:]
    
    #Extracting dates
    dates = re.findall(pattern,data)
    
    #Making dataframe
    df = pd.DataFrame({'message': message,'date':dates})
    df['date'] = pd.to_datetime(df['date'],format='%d/%m/%y, %H:%M - ')
    
    #Making different columns for users and messages
    user = []
    message = []
    for messages in df['message']:
        row = re.split('([\w\W]+?):\s', messages)
        if row[1:]:
            user.append(row[1])
            message.append(" ".join(row[2:]))
        else:
            user.append('notification')
            message.append(row[0])
    
    df['user'] = user
    df['message'] = message
    
    #Extracting dates,day,month,year,hour,minute
    df['dates'] = df['date'].dt.date 
    df['year'] = df['date'].dt.year
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df