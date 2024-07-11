# -*- coding: utf-8 -*-

from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(given_user,df):

    if given_user != 'Overall':
        df = df[df['user'] == given_user]

    # fetch the number of messages
    total_message = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    total_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return total_message,len(words),total_media_messages,len(links)

def users_active_percentage(df):
    x = df['user'].value_counts()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'percent'})
    return x,df

#def create_wordcloud(selected_user,df):

   # f = open('stop_hinglish.txt', 'r')
   # stop_words = f.read()

   # if selected_user != 'Overall':
   #     df = df[df['user'] == selected_user]

    #temp = df[df['user'] != 'group_notification']
   # temp = temp[temp['message'] != '<Media omitted>\n']

   # def remove_stop_words(message):
        #y = []
       # for word in message.lower().split():
         #   if word not in stop_words:
          #      y.append(word)
        #return " ".join(y)

   # wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
   # temp['message'] = temp['message'].apply(remove_stop_words)
   # df_wc = wc.generate(temp['message'].str.cat(sep=" "))
   # return df_wc

def twenty_most_common_words(given_user,df):

    if given_user != 'Overall':
        df = df[df['user'] == given_user]

    clean_df = df[df['user'] != 'notification']
    clean_df = clean_df[clean_df['message'] != '<Media omitted>\n']

    words = []
    stopwords = ['ha', 'haa', 'haan', 'na', 'naa', 'nhi', 'keno', 'kyano', 'kano', 'bhai', 'vai', 'ei', 'e', 'ki',
                  're', 'ami', 'tui', 'tumi', 'amay', 'amake', 'toke', 'amake', 'kor', 'korte', 'hobe', 'acha', 'accha',
                  'achha', 'achchha', 'khub', 'aage', 'aaj', 'aj', 'kal', 'kaal', 'kya', 'kyu', 'kyun', 'tu', 'tereko',
                  'ko', 'hi', 'se', 'to', 'toh', 'hoga', 'the', 'is', 'hai', 'of', 'you', 'hum', 'main', 'and', 
                  'bhi','theke','bol','ja','ta','er','o','kore','ar','aar','eta','ota','tai','kichu',
                  'ohh','uff','sob','shob','son','shon','kichhu','abar','ebar','but','te','amar','amr',
                  'sathe','shathe','bole','hobe','hbe','tho','tor','nei','ekta','thik','hoy','hoye',
                  'jani','oi','tr','r','or','kono','tao','ache','de','ke','ache','message','deleted',
                  'bhalo','this','that','niye','de','noy','was','ekhon','akhon','gulo','j','a',
                  'keu','k','?','edited>','<this','hmm']
    for message in clean_df['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    common_df = pd.DataFrame(Counter(words).most_common(20))
    return common_df

def emoji_analyzer(given_user,df):
    if given_user != 'Overall':
        df = df[df['user'] == given_user]

    emojis = []
    for message in df['message']:
        emojis.extend([x for x in message if x in emoji.EMOJI_UNICODE['en']])

    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojis_df

def monthly_timeline(given_user,df):

    if given_user != 'Overall':
        df = df[df['user'] == given_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(given_user,df):

    if given_user != 'Overall':
        df = df[df['user'] == given_user]

    daily_timeline = df.groupby('dates').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(given_user,df):

    if given_user != 'Overall':
        df = df[df['user'] == given_user]

    return df['day_name'].value_counts()

def month_activity_map(given_user,df):

    if given_user != 'Overall':
        df = df[df['user'] == given_user]

    return df['month'].value_counts()

def activity_map(given_user,df):

    if given_user != 'Overall':
        df = df[df['user'] == given_user]

    user_map = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_map

