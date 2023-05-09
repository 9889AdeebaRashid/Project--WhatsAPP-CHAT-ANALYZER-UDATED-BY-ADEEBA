import streamlit as st 
import preprocessor,helper 
import matplotlib.pyplot as plt 
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file") 
if uploaded_file is not None: 
    bytes_data = uploaded_file.getvalue() 
    data = bytes_data.decode("utf-8") 
    df = preprocessor.preprocess(data)

st.dataframe(df)

#fetch  unique users
user_list = df['user'].unique().tolist()
user_list.sort()
user_list.insert(0,"Overall")

selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

if st.sidebar.button("Show Analysis"):
    # stats area
    num_messages, words, num_media_messages, num_links,num_totaltime = helper.fetch_stats(selected_user,df)
    st.title("Top Statistics")
    col1, col2, col3, col4,col5 = st.columns(5)


    with col1:
        st.header("Total Messages")
        st.title(num_messages)
    with col2:
        st.header("Total Words")
        st.title(words)
    with col3:
        st.header("Media Shared")
        st.title(num_media_messages)
    with col4:
        st.header("Links Shared")
        st.title(num_links)
    with col5:
        st.header("Total Time Spent")
        st.title(num_totaltime)

    # monthly timeline
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'],color='orange')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # daily timeline
    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    #weekly timeline
    st.title("Weekly Timeline")
    weekly_timeline = helper.weekly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(weekly_timeline['only_date'], daily_timeline['message'], color='blue')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    # activity map
    st.title('Activity Map')
    col1,col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    plt.xticks(rotation='vertical')
    st.pyplot(fig)



    # finding the busiest users in the group(Group level)
    if selected_user == 'Overall':
        st.title('Most busy users')
        x,new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # most common words
    most_common_df = helper.most_common_words(selected_user,df)
    fig,ax = plt.subplots()
    ax.bar(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title('Most Common Words')