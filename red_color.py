import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib.pyplot as plt
import math

# TODO CHANGE ME 
url_for_the_code =  f'https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=en&fromDate=01.10.2023&toDate=31.10.2023&mode=0'


# BASIC EXAMPLES
# URLS to get them pls go to : https://www.oref.org.il/12481-en/Pakar.aspx -> inspect elements -> network -> pick city -> check GetAlarmsHistory.aspx -> take url
basic_url = f'https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=en&fromDate=01.10.2023&toDate=31.10.2023&mode=0'
url_ashdod = f'{basic_url}&city_0=Ashdod%20-%20Alef,%20Bet,%20Dalet,%20Heh&city_1=Ashdod%20-%20Gimmel,%20Vav,%20Zain&city_2=Ashdod%20-%20Het,%20Tet,%20Yod,%20Yod%20Gimmel,%20Yod%20Dalet,%20Te*&city_3=Ashdod%20-%20Yod%20Alef,%20Yod%20Bet,%20Tet%20Vav,%20Yod%20Zain,%20Marina,%20City'
url_rishon = f'{basic_url}&city_0=Rishon%20LeZion%20-%20East&city_1=Rishon%20LeZion%20-%20West'
url_beersheva = f'{basic_url}&city_0=Beer%20Sheva%20-%20East&city_1=Beer%20Sheva%20-%20North&city_2=Beer%20Sheva%20-%20South&city_3=Beer%20Sheva%20-%20West'
url_all_city = f'{basic_url}'
url_tel_aviv = f'{basic_url}&city_0=Tel%20Aviv%20-%20Across%20the%20Yarkon&city_1=Tel%20Aviv%20-%20City%20Center&city_2=Tel%20Aviv%20-%20East&city_3=Tel%20Aviv%20-%20South%20and%20Jaffa'


class redColor:
    def __init__(self, url) -> None:
        self.url = url
    
    def get_red_color(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            return {"error": f"{res.status_code}, {res.content}"}
        res = response.json()
        return [resp["alertDate"] for resp in res]

    def clean_data(self, data):
        self.df_date = pd.DataFrame(data, columns=['alertDate'])
        self.df_date = self.df_date.drop_duplicates()
        self.format_data()
        
        self.incident_count_date['alertDate'] = self.incident_count_date['alertDate'].dt.round('2min')
        self.incident_count_date['Minutes'] = self.incident_count_date['alertDate'].dt.minute 
        self.incident_count_date['Hours'] = self.incident_count_date['alertDate'].dt.hour 
        self.incident_count_date['Date'] = self.incident_count_date['alertDate'].dt.date 
        self.df_date['Day_of_Week'] = self.incident_count_date['alertDate'].dt.strftime('%A')
    
    def format_data(self):
        self.incident_count_date = self.df_date.groupby(['alertDate']).size().reset_index(name='Incident Count')
        self.incident_count_date["temp_alertDate"] = self.incident_count_date['alertDate']
        self.incident_count_date['alertDate'] = pd.to_datetime(self.incident_count_date['alertDate'], format='%Y-%m-%dT%H:%M:%S')

    def plot_minutes_against_incident_count(self):
        self.incident_count_date_minutes = self.incident_count_date.groupby(['Minutes']).agg({'Incident Count': 'sum'}).reset_index()
        plt.figure(figsize=(10, 6))
        plt.bar(self.incident_count_date_minutes["Minutes"], self.incident_count_date_minutes["Incident Count"], width=0.5) 
        plt.xlabel('Minutes')
        plt.ylabel('Incident Count')
        plt.title('Shooting Incidents by Time (Incident Count vs. Minutes)')
        plt.xticks(range(0, 60, 2))
    
    def plot_hours_against_incident_count(self):
        self.incident_count_date_hours = self.incident_count_date.groupby(['Hours']).agg({'Incident Count': 'sum'}).reset_index()
        plt.figure(figsize=(10, 6))
        plt.bar(self.incident_count_date_hours["Hours"], self.incident_count_date_hours["Incident Count"], width=0.5) 
        plt.xlabel('Hours')
        plt.ylabel('Incident Count')
        plt.title('Shooting Incidents by Time (Incident Count vs. Hours)')
        plt.xticks(range(0, 24))
    
    def plot_days_against_incident_count(self):
        incident_count_by_day = self.df_date['Day_of_Week'].value_counts().reset_index()
        incident_count_by_day.columns = ['Day_of_Week', 'Incident Count']

        days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        incident_count_by_day['Day_of_Week'] = pd.Categorical(incident_count_by_day['Day_of_Week'], categories=days_of_week, ordered=True)
        incident_count_by_day = incident_count_by_day.sort_values('Day_of_Week')

        plt.figure(figsize=(12, 6))
        plt.bar(incident_count_by_day["Day_of_Week"], incident_count_by_day["Incident Count"], width=0.5) 
        plt.xlabel('Days')
        plt.ylabel('Incident Count')
        plt.title('Shooting Incidents by Time (Incident Count vs. Days)')


def main():
    red_color = redColor(url_for_the_code) # TOTO REPLACE ME WITH YOUR URL
    data = red_color.get_red_color()
    red_color.clean_data(data)
    red_color.plot_minutes_against_incident_count()
    red_color.plot_hours_against_incident_count()
    red_color.plot_days_against_incident_count()
    plt.show()

if __name__ == '__main__':
    main()



# use calander to transform the dates to days and count which days had the most incidents





