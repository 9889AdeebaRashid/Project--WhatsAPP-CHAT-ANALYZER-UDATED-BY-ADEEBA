#!/usr/bin/env python
# coding: utf-8

# # first we'll do data-preprocessing.
# our chat is in text file, i want to extract that text file and will convert it into pandas data frame.
# concepts used here will be Regular Expression.
# 

# In[1]:


#I have used two libraries- regular expression and pandas

import re
import pandas as pd


# In[2]:


#opening file using file handling in python

f = open('WhatsApp Chat with five Friends.txt','r',encoding='utf-8')


# In[3]:


#this will read all the content of file in the form of string and store that in data variable
data = f.read()


# In[4]:


print(data)


# In[5]:


#whole whatsapp chat is stored in the form of a string and here we're just verifying the data type of our chat data

print(type(data))


# Now I want to convert this in Pandas Data Frame. Pandas is a library in Python.

# now i will write date in different column and user name in different column

# basically, i want to create a new data frame which will contain two columns namely Message and Date. Message will contain   
# user name and the content of message. For that I have written a regular expression string.

# In[6]:


#writing the regular expression of string

pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'


# You can also use regex101.com, if you dont know how to write regular expression

# In[7]:


messages = re.split(pattern, data)[1:] #here I've used string slicing so that empty list can be removed
len(messages)


# In[8]:


#Extracting dates

dates = re.findall(pattern, data)
dates


# Now I have two lists. One containing username and messages. The other list containing the date at which the message was sent.

# In[9]:


#now I've created a pandas dataframe which contains two columns namely user_message and the other message_date

df = pd.DataFrame({'user_message': messages, 'message_date': dates})


# In[10]:


# convert message_date explicitly to datetime

df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')


# In[11]:


df.rename(columns={'message_date': 'date'}, inplace=True)


# In[12]:


df.head() #head will show top 5 messages


# From the output, I can see that the user name and message is in same column. So, I want to bifurcate user name and column.

# In[13]:


df.shape #it displays total rows and columns currently


# In[14]:


users = []
messages = []
for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s', message) #splitting on this pattern so that is username:string is there, split it.
    if entry[1:]:  # user name
        users.append(entry[1]) #creating a list and inserting all the users
        messages.append(" ".join(entry[2:])) #second part of the string(after colon), adding that in messages
    else:
        users.append('group_notification') #if any string doesn't contain colon, then it'll be a group notification, 
                                           #so appending that in users
        messages.append(entry[0]) #rest will remain as it is in messages
        
df['user'] = users #creating new column named user
df['message'] = messages #creating new column named message
df.drop(columns=['user_message'], inplace=True)

df.head()


# Now, it can be seen that date, user and message are bifurcated

# Now, I'll further bifurcate my date column in year, month and date. After that I'll move to streamlit to convert it into web
# application.

# In[15]:


#extracting year

df['year'] = df['date'].dt.year


# In[16]:


df.head()


# Now it can be seen from the output that a new column named "year" is also present. Similarly, I'll do it for month, day, hour
# and minute.

# In[17]:


df['month'] = df['date'].dt.month_name()


# In[18]:


df['day'] = df['date'].dt.day


# In[19]:


df['hour'] = df['date'].dt.hour


# In[20]:


df['minute'] = df['date'].dt.minute


# In[21]:


df.head()


# # Now our pre-processing is done. Our data frame is ready.

# In[22]:


df[df['user'] == 'Adeeba'].shape


# In[23]:


words = []
for message in df['message']:
    words.extend(message.split())


# In[24]:


len(words)


# In[25]:


df[df['user'] == 'Adeeba'].shape


# In[26]:


for message in df['message']:
    print(message) #it will print all the messages


# In[27]:


words = []
for message in df['message']:
    words.extend(message.split())
    


# In[28]:


len(words) #total number of words typed by all members in the group


# In[29]:


pip install urlextract


# In[30]:


from urlextract import URLExtract

extractor = URLExtract()
urls = extractor.find_urls("Let's have URL stackoverflow.com as an example, http://facebook.com, ftp://url.in")
#fetching urls
urls


# In[31]:


links = []

for message in df['message']:
    print(extractor.find_urls(message)) #I've made an extractor object and whenever any particular message has a link or url,
                                #then this function will extract that and put that in a list else it will give an empty list
        


# In[32]:


links = []

for message in df['message']:
    links.extend(extractor.find_urls(message))
    
links #this will give a list of all links


# In[33]:


len(links)


# In[34]:


df


# In[35]:


x = df['user'].value_counts().head() #top 5 busy users in the group


# In[36]:


round((df['user'].value_counts()/df.shape[0])*100,2) #percentage of message done by each user


# In[37]:


round((df['user'].value_counts()/df.shape[0])*100,2).reset_index() #converting it into data frame


# In[38]:


round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})


# In[39]:


#plotting bar chart

import matplotlib.pyplot as plt


# In[40]:


name = x.index
count = x.values


# In[41]:


plt.bar(name,count)
plt.xticks(rotation='vertical')
plt.show()


# In[42]:


# remove group notification

df[df['user'] == 'group_notification']


# In[43]:


temp = df[df['user'] != 'group_notification']
temp = temp[temp['message'] != '<Media omitted>\n']


# In[44]:


f = open('stop_hinglish.txt','r')
stop_words = f.read()
print(stop_words)


# In[45]:


words = []

for messages in temp['message']:
    for word in message.lower().split():
        if word not in stop_words:
            words.append(word)
            
    words.extend(message.split())


# In[46]:


from collections import Counter
Counter(words) #calculating the frequency of each word


# In[47]:


from collections import Counter
pd.DataFrame(Counter(words).most_common(4))


# It can be seen that most of them are stop words. Stop words are used in sentence formation but they do not have an appropriate
# meaning. So, we need to remove group notification meessages like "someone left the group", "someone changed the group icon" etc. then remove media omitted message. Finally remove stop words and repeat this process.

# In[48]:


df['month_num'] = df['date'].dt.month


# In[49]:


timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index() 
timeline


# In[50]:


#merging year and month column

time = []
for i in range(timeline.shape[0]):
    time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
time


# In[51]:


timeline['time'] = time
timeline


#  All this processing is donne to keep time on x axis and message on y axis respectively.

# In[52]:


plt.plot(timeline['time'],timeline['message'])
plt.xticks(rotation='vertical')
plt.show()


# In[53]:


#extracting date

df['only_date'] = df['date'].dt.date


# In[54]:


#displaying daily timeline of the group members

daily_timeline = df.groupby('only_date').count()['message'].reset_index()
daily_timeline


# In[55]:


plt.figure(figsize=(18,10))

plt.plot(daily_timeline['only_date'],daily_timeline['message'])


# In[56]:


df.head()


# In[57]:


df['day_name'] = df['date'].dt.day_name()


# In[58]:


df['day_name'].value_counts() #this tells the day at which the group members were most active on


# In[59]:


df['month'].value_counts()


# # Now I'll make a heap map which will signify at what time the users were most active and least active on WhatsApp during the whole week. 
# 
# x-axis shows time period
# y-axis shows the days
# 
# The lighter the shade, more active are the users.
# The darker the shade, less active are the users.

# In[60]:


period = []
for hour in df[['day_name','hour']]['hour']:
    if hour == 23:
        period.append(str(hour) + "-" + str('00'))
    elif hour == 0:
        period.append(str('00') + "-" + str(hour+1))
    else:
        period.append(str(hour) + "-" + str(hour+1))


# In[61]:


df['period'] = period


# In[62]:


df.sample(5)


# Now, it can be seen that a new column named period is also in the dataframe. so, if there's 10 then period will be 10-11 and so on. After this, Plot a pivot table.

# In[63]:


get_ipython().system('pip install seaborn')


# In[64]:


import seaborn as sns


# In[65]:


df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)


# In[66]:


plt.figure(figsize=(20,6))
sns.heatmap(df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0))
#there might be any day in any particular period where no msg will be there, so fillna() will fill that value with 0.
plt.yticks(rotation='horizontal')
plt.show()


# # So, this was the over all DETAILED ORIENTED ANALYSIS.
