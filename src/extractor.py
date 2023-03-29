import pandas as pd
import requests
import time
import json
from datetime import datetime
from tqdm import tqdm


class Extractor:
    def __init__(self, lat, lon, start, end, api_key, units='metric'):
        self.api_calls = 0
        self.max_calls = 900
        self.calls_per_minute = 50
        self.dates_to_collect = pd.date_range(start, end, freq='D').astype(int) // 10 ** 9
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.units = units
        self.start_time = None
        self.data = None
        self.last_collected_date = datetime.fromtimestamp(self.dates_to_collect[0]).date()
        print(f"Collecting data from {self.last_collected_date} to {end} ...")

    def url(self, date):
        return f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={self.lat}&lon={self.lon}&dt={date}&appid={self.api_key}&units={self.units}"

    def start_extraction(self):
        self.start_time = time.time()
        return self.extract()

    def extract(self):
        data = []
        for date in tqdm(self.dates_to_collect):
            try:
                mins = (time.time() - self.start_time) / 60 + 1
                current_cpm = self.api_calls / mins
                # print(f"Current CPM: {current_cpm}")
                # print(f"Current API calls: {self.api_calls} in {mins:.2f} minutes")
                if current_cpm > self.calls_per_minute:
                    time_to_wait = 60 - (time.time() - self.start_time) % 60
                    # print(f"Waiting {time_to_wait} seconds")
                    time.sleep(time_to_wait)

                if self.api_calls > self.max_calls:
                    print("API calls exceeded")
                    print(f"Last date call {date}")
                    break

                response = requests.get(self.url(date))

                if response.status_code == 200:
                    data.append(response.json())
                    self.api_calls += 1
                else:
                    print(f"Error: {response.status_code}")
                    break
            except Exception as e:
                print(e)
                break
            finally:
                self.last_collected_date = datetime.fromtimestamp(date).date()

        self.data = data

    @property
    def to_df(self):
        data_to_df = [response["data"][0] for response in self.data]
        df = pd.DataFrame(data_to_df)
        return df


start = "2020-07-09"
end = "2020-12-31"

api_key = "YOUR_API_KEY"
lat = -23.555771
lon = -46.639557

extractor = Extractor(lat, lon, start, end, api_key)
extractor.start_extraction()
df = extractor.to_df

filename = f"{start}_{extractor.last_collected_date}.csv"
df.to_csv(f"../data/{filename}", index=False)
