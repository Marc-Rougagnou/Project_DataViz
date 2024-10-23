import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%% Introduction du dataset

st.markdown("<h1 style='color: orange;'><strong>Uber database project of April 14</strong></h1>", unsafe_allow_html=True)

st.write("This is the result of the notebook that we have done in class during September 2024, when the professor show us how to use the librairies.")

#%% Ouverture

st.markdown("<h3 style='color: Darkorange;'><strong>Link to the dataset</strong></h3>", unsafe_allow_html=True)

path = os.path.join(os.path.dirname(__file__), 'uber-raw-data-apr14.csv')
df = pd.read_csv(path, delimiter = ',')
df=df[:80000]

st.write("With this code, I load the dataset, then take only part of it, as it takes too long to convert.")

code_split = '''
    path = "uber-raw-data-apr14.csv" 
    df = pd.read_csv(path, delimiter = ',')
    df=df[:80000]
    '''
st.code(code_split, language='python')

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="**Dowload the dataset**",
    data=csv,
    file_name=path,
    mime="text/csv")


#%% 
st.markdown("<h2 style='color: orange;'>Start of the exploration of the dataset</h2>", unsafe_allow_html=True)

def convertir_datetime(df):
    df['Date/Time'] = df['Date/Time'].map(pd.to_datetime)
    return df

def get_dom(dt):
    return dt.day

def get_weekday(dt):
    return dt.weekday() #give the number of day Monday=0 sunday=6

def get_hour(dt):
    return dt.hour

def count_rows(rows):
    return len(rows)

st.write(df.head())
st.write("If you click on that buttom it will convert into a date format !!")
st.write("I will also create 3 columns to have the day, the weekday and the hour of uber trip.")


if st.button('Convert and Create'):
    with st.spinner('In progress...'):
        df = convertir_datetime(df)
        df['day'] = df['Date/Time'].map(get_dom)
        df['weekday'] = df['Date/Time'].map(get_weekday)
        df['hour'] = df['Date/Time'].map(get_hour)
    st.success('Conversion finish and column created!')
    st.write("After conversion there it is the 5 first row of the dataset")
    st.write(df.head())


#%% début des graphs

    by_date = df.groupby('day').apply(count_rows)
    
    full_range = pd.Series(0, index=range(1, 31))  # Initialize with zeros for all days
    full_range.update(by_date)  # Update with actual counts
    
    st.markdown("<h4 style='color: Darkorange;'>1. Histogram for frequency by day of the month</h4>", unsafe_allow_html=True)
    plt.figure(figsize=(25, 15))
    hist = df["day"].plot.hist(bins=30, rwidth=0.8, range=(0.5, 30.5), title="Frequency by DoM - Uber - April 2014")
    plt.xlabel('Days of the month')
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("<h4 style='color: Darkorange;'>2. Line plot for frequency by day of the month</h4>", unsafe_allow_html=True)
    plt.title('Line plot - Uber - April 2014')
    plt.xlabel('Days of the month')
    plt.ylabel('Frequency')
    plt.plot(full_range.index, full_range.values)
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("<h4 style='color: Darkorange;'>3. Bar plot for frequency by day of the month</h4>", unsafe_allow_html=True)
    plt.figure(figsize=(25, 15))
    plt.bar(full_range.index, full_range.values)
    plt.xticks(range(1, 31), full_range.index)
    plt.xlabel('Date of the month', fontsize=20)
    plt.ylabel('Frequency', fontsize=20)
    plt.title('Frequency by DoM - Uber - April 2014', fontsize=20)
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("<h4 style='color: Darkorange;'>4. Histogram for hours of the day</h4>", unsafe_allow_html=True)
    plt.hist(df['hour'], bins=24, range=(-0.5, 24))
    plt.xlabel('Hour of the day')
    plt.ylabel('Frequency')
    plt.title('Frequency by Hour - Uber - April 2014')
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("<h4 style='color: Darkorange;'>5. Histogram for days of the week</h4>", unsafe_allow_html=True)
    plt.hist(df['weekday'], bins=7, rwidth=0.8, range=(-0.5, 6.5))
    plt.xlabel('Day of the week')
    plt.ylabel('Frequency')
    plt.title('Frequency by Day of the Week - Uber - April 2014')
    plt.xticks(np.arange(7), 'Mon Tue Wed Thu Fri Sat Sun'.split())
    st.pyplot(plt)
    plt.clf()
    
    df2 = df.groupby(['weekday', 'hour']).apply(count_rows).unstack()
    
    st.markdown("<h4 style='color: Darkorange;'>The first few rows of the heatmap data</h4>", unsafe_allow_html=True)
    st.write(df2.head())
    
    st.markdown("<h4 style='color: orange;'>Heatmap of the dataset</h4>", unsafe_allow_html=True)
    plt.figure(figsize=(10, 6))
    heatmap = sns.heatmap(df2, linewidths=0.5)
    plt.title('Heatmap by Hour and Weekdays - Uber - April 2014', fontsize=15)
    heatmap.set_yticklabels(('Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'), rotation='horizontal')
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("<h4 style='color: Darkorange;'>7. Latitude histogram</h4>", unsafe_allow_html=True)
    plt.hist(df['Lat'], bins=100, range=(40.5, 41), color='r', alpha=0.5, label='Latitude')
    plt.xlabel('Latitude')
    plt.ylabel('Frequency')
    plt.title('Latitude - Uber - April 2014')
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("<h4 style='color: Darkorange;'>8. Longitude histogram</h4>", unsafe_allow_html=True)
    plt.hist(df['Lon'], bins=100, range=(-74.1, -73.9), color='g', alpha=0.5, label='Longitude')
    plt.xlabel('Longitude')
    plt.ylabel('Frequency')
    plt.title('Longitude - Uber - April 2014')
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("<h4 style='color: Darkorange;'>9. Combined Latitude/Longitude histograms</h4>", unsafe_allow_html=True)
    plt.figure(figsize=(10, 10), dpi=100)
    plt.title('Longitude and Latitude Distribution - Uber - April 2014', fontsize=15)
    plt.hist(df['Lon'], bins=100, range=(-74.1, -73.9), color='g', alpha=0.5, label='Longitude')
    plt.legend(loc='best')
    plt.twiny()
    plt.hist(df['Lat'], bins=100, range=(40.5, 41), color='r', alpha=0.5, label='Latitude')
    plt.legend(loc='upper left')
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("<h4 style='color: Darkorange;'>10. Scatter plot for Latitude and Longitude</h4>", unsafe_allow_html=True)
    plt.figure(figsize=(15, 15), dpi=100)
    plt.title('Scatter plot - Uber - April 2014')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.scatter(df['Lat'], df['Lon'], s=0.8, alpha=0.4)
    plt.ylim(-74.1, -73.8)
    plt.xlim(40.7, 40.9)
    st.pyplot(plt)
    plt.clf()

