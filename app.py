# -*- coding: utf-8 -*-

#importing dependencies

import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

#Creating the sidebar and the notice statement
st.sidebar.title("Whatsapp Chat Analyzer")
st.header("Your Chat Time should be in 24 hours Format")
#Getting the dataframe
file = st.sidebar.file_uploader("Export Your Chat Without Media, Covert To .txt File And Upload It")
if file is not None:
    bytes = file.getvalue()
    data = bytes.decode('utf-8')
    df = preprocessor.preprocessing(data)
    
    
    #Getting the users
    users = df['user'].unique().tolist()
    users.remove("notification")
    users.sort()
    users.insert(0,"Overall")
    given_user = st.sidebar.selectbox("Get Analysis For",users)
    
    #Providing analysis button
    if st.sidebar.button("Give Analysis"):
        # Stats Area
        total_message, words, total_media_messages, num_links = helper.fetch_stats(given_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)
        #For column1
        with col1:
            st.header("Number of Message")
            st.title(total_message)
         #For column2
        with col2:
           st.header("Total Words")
           st.title(words)
         #For column3
        with col3:
           st.header("Media Shared")
           st.title(total_media_messages)
         #For column4
        with col4:
           st.header("Total Links Shared")
           st.title(num_links)

       # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(given_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

       # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(given_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['dates'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

     
        #Checking activites
        st.title("Activity Analysis")
        col1,col2 = st.columns(2)
        with col1:
           st.header("Most busy day")
           busy_day = helper.week_activity_map(given_user,df)
           fig,ax = plt.subplots()
           ax.bar(busy_day.index,busy_day.values,color='red')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

        with col2:
           st.header("Most busy month")
           busy_month = helper.month_activity_map(given_user, df)
           fig, ax = plt.subplots()
           ax.bar(busy_month.index, busy_month.values,color='green')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_map = helper.activity_map(given_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_map)
        st.pyplot(fig)

       # finding the busiest users in the group(Group level)
        if given_user == 'Overall':
           st.title('Users Activeness in the Chat')
           x,new_df = helper.users_active_percentage(df)
           fig, ax = plt.subplots()

           col1, col2 = st.columns(2)

           with col1:
               ax.bar(x.index, x.values,color='magenta')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
           with col2:
               st.dataframe(new_df)

       

       # Getting twenty most common words
        common_df = helper.twenty_most_common_words(given_user,df)

        fig,ax = plt.subplots()

        ax.barh(common_df[0],common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Twenty Most commmon words')
        st.pyplot(fig)


       