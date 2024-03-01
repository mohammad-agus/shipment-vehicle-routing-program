from datetime import datetime, date, time
import re
from Schedule import Schedule


a = datetime(2024,3,2,8,14)
b = datetime(2024,3,2,19,14)

c = Schedule.get_vehicle_time_window(vehicles=2, idx=0, datetime_to_epoch_function=Schedule.to_epoch)


print(c)
