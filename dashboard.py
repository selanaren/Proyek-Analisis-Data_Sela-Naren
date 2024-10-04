import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

def create_weather_holiday_df(df, isHolidaybyInt):
    weather_holiday_df = df[df["holiday"] == isHolidaybyInt].groupby(["weathersit"])["cnt"].sum().sort_values(ascending=False).reset_index()
    if not (weather_holiday_df["weathersit"] == 4).any():
        new_row = pd.DataFrame({"weathersit": [4], "cnt": [0]})
        weather_holiday_df = pd.concat([weather_holiday_df, new_row], ignore_index=True)

    weather_holiday_df.rename(columns={"weathersit": "index_cuaca", "cnt": "jumlah_pengguna"}, inplace=True)

    return weather_holiday_df

def create_byHourGroup_df(df):
    df["hr_group"] = df.hr.apply(lambda x: "Dini Hari" if x >= 0 and x < 6
                                  else ("Pagi Hari" if x >= 6 and x < 11
                                        else "Siang Hari" if x >= 11 and x < 15
                                        else "Sore Hari" if x>= 15 and x < 18
                                        else "Malam Hari"))

    byHourGroup_df = df.groupby(by="hr_group")["cnt"].sum().reset_index()
    byHourGroup_df.rename(columns={"hr_group": "categories", "cnt": "jumlah_pengguna"}, inplace=True)

    return byHourGroup_df

# Load datasets
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

# Sort values and convert date column
column = "dteday"
day_df.sort_values(by=column, inplace=True)
day_df.reset_index(drop=True, inplace=True)
hour_df.sort_values(by=column, inplace=True)
hour_df.reset_index(drop=True, inplace=True)

day_df[column] = pd.to_datetime(day_df[column])
hour_df[column] = pd.to_datetime(hour_df[column])

# Get date range
min_date = day_df[column].min()
max_date = day_df[column].max()

with st.sidebar:
    st.image("bike.jpeg")

    # Date input for selecting time range
    start_date, end_date = st.date_input(label="Time", min_value=min_date, max_value=max_date, value=[min_date, max_date])

# Convert start_date and end_date to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter dataframes by selected date range
main_df = day_df[(day_df[column] >= start_date) & (day_df[column] <= end_date)]
second_df = hour_df[(hour_df[column] >= start_date) & (hour_df[column] <= end_date)]

# Create dataframes for visualizations
weather_holiday_df = create_weather_holiday_df(main_df, 0)
byHourGroup_df = create_byHourGroup_df(second_df)

# Dashboard content
st.header("Bike Sharing Dashboard :sparkles:")

# Holiday pie charts
st.subheader("Holiday Weather Impact")

col1, col2 = st.columns(2)

labels_detail = ['Clear or Partly Cloudy', 'Mist and/or Cloudy', 'Light Rain and/or Thunderstorm or Light Snow', 'Heavy Rain or Snow and Fog']

# Create pie chart for holiday
fig1, ax1 = plt.subplots()
size = weather_holiday_df["jumlah_pengguna"]
pie1 = ax1.pie(size, startangle=0)
ax1.set_title("Jumlah Pengguna Sepeda di Setiap Cuaca\nPada Hari Libur Tahun 2011-2012", ha="center")
ax1.legend(pie1[0], labels_detail, bbox_to_anchor=(0.65, -0.05), loc="lower right", bbox_transform=plt.gcf().transFigure)
col1.pyplot(fig1)

# Barplot for time of day analysis
st.subheader("Time and Bike Bounce Correlation")

fig3 = plt.figure(figsize=(10, 5))
sns.barplot(y="jumlah_pengguna", x="categories", hue="categories", data=byHourGroup_df.sort_values(by="jumlah_pengguna", ascending=False), dodge=False)
plt.title("Jumlah Total Pengguna di Tiap Kelompok Jam", loc="center", fontsize=17)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis="x", labelsize=12)
plt.legend(title="Kategori Waktu")
st.pyplot(fig3)