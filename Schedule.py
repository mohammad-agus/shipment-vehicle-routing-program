import folium
from openrouteservice.optimization import Job, Vehicle
from openrouteservice import Client, convert
import re
import csv
from typing import Union
from datetime import datetime, date, time

# Load API key
from dotenv import dotenv_values
api_key = dotenv_values(".env")["API_KEY"]


class Schedule:

    @classmethod
    def to_unix_timestamp(cls, date_time: datetime) -> datetime.timestamp:
        return date_time.timestamp()

    @classmethod
    def get_vehicle_time_window(cls, vehicles: int, idx: int, datetime_to_epoch_function) -> list[datetime]:
        p = r"^(2[0-9]{3})-0?([1-9]|1[0-2])-0?([1-9]|[1-3][0-9]) 0?([1-9]|[1-2][0-9]):0?([0-9]|[1-5][0-9])$"
        while True:
            try:
                print('Date and time format: "YYYY-MM-DD HH:mm"')
                if vehicles > 1:
                    print(f'Input shipment schedule (date & time) of vehicle {idx+1} (in  format):')
                else:
                    print('Input shipment schedule (date & time) of the vehicle in "YYYY-MM-DD HH:mm" format:')
                dt1 = input(f"Begin: ")
                dt1 = re.match(pattern=p, string=dt1)
                if dt1 == None:
                        print("Please input a valid datetime!")
                        continue
                ts1 = datetime(int(dt1.group(1)), int(dt1.group(2)), int(dt1.group(3)), int(dt1.group(4)), int(dt1.group(5)), 0)
                dt2 = input(f"End: ")
                dt2 = re.match(pattern=p, string=dt2)
                if dt2 == None:
                        print("Please input a valid datetime!")
                        continue
                ts2 = datetime(int(dt2.group(1)), int(dt2.group(2)), int(dt2.group(3)), int(dt2.group(4)), int(dt2.group(5)), 0)
                if ts1 >= ts2:
                     print("Invalid input: datetime beginning >= datetime ending!")
                     continue
                return [datetime_to_epoch_function(ts1), datetime_to_epoch_function(ts2)]
            except ValueError:
                print("Please input a valid datetime!")
                pass
    