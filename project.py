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
    def to_epoch(cls, date_time: datetime):
        return date_time.timestamp()

    @classmethod
    def get_shipment_datetime(cls, vehicles: int, idx: int) -> date:
        p = r"^(2[0-9]{3})-0?([1-9]|1[0-2])-0?([1-9]|[1-3][0-9]) 0?([1-9]|[1-2][0-9]):0?([0-9]|[1-5][0-9])$"
        while True:
            try:
                if vehicles > 1:
                    print(f"Input shipment schedule (date & time) of vehicle {idx+1} in 'YYYY-MM-DD HH:mm' format:")
                else:
                    print("Input shipment schedule (date & time) of the vehicle in 'YYYY-MM-DD HH:mm' format:")
                dt = input(">> ")
                if dt := re.match(pattern=p, string=dt):
                    return datetime(int(dt.group(1)), int(dt.group(2)), int(dt.group(3)), int(dt.group(4)), int(dt.group(5)), 0)
                print("Please input a valid datetime!")
                pass
            except ValueError:
                print("Please input a valid datetime!")
                pass



def main():

    data: list = get_csv_data()
    client = Client(key=api_key)
    route_map = folium.Map(location=get_shipment_start_point(data), tiles="openstreetmap", zoom_start=14)

    folium.Marker(location=get_shipment_start_point(data), icon=folium.Icon(color="red")).add_to(route_map)
    for coord in get_shipment_points(data):
        folium.Marker(location=coord).add_to(route_map)

    jobs = []
    for i, loc in enumerate(get_job_list(data)):
        jobs.append(Job(id=i, location=loc["location"][::-1], amount=loc["amount"]))

    number_of_vehicles = get_vehicle_number()
    vehicles = get_vehicles(data, number_of_vehicles)
    optimized = client.optimization(jobs=jobs, vehicles=vehicles, geometry=True)
    for route in optimized['routes']:
        folium.PolyLine(locations=[route[::-1] for route in
                                   convert.decode_polyline(route['geometry'])['coordinates']]).add_to(route_map)
    print(optimized)

    # route_map.save("route_map.html")


def get_coord(location: dict) -> list:
    return [location["lat"], location["long"]]


def get_shipment_points(dt: list) -> list:
    return [[loc["lat"], loc["long"]] for loc in dt[2:]]


def get_shipment_start_point(dt: list) -> list:
    return [dt[0]["lat"], dt[0]["long"]]


def get_shipment_end_point(dt: list) -> list:
    return [dt[1]["lat"], dt[1]["long"]]


def get_job_list(dt: list) -> list:
    return [{"location": [job["lat"], job["long"]], "amount": job["delivery_amount"]} for job in dt[2:]]


def get_job_index(dt: list) -> list:
    return [i.get("id") for i in dt[2:]]


def get_csv_data() -> list[dict]:
    while True:
        try:
            file_path = input("Input csv file: ")
            with open(file_path) as input_data:
                dt = csv.DictReader(input_data)
                return [{"id": row["id"], "lat": float(row["lat"]), "long": float(row["long"]),
                         "delivery_amount": [int(row["delivery_amount"])]} for row in dt]
        except FileNotFoundError:
            print("Please input a valid csv file!")
            pass


def get_vehicles(dt, nums_of_vehicle) -> list:
    vehicles: list = [Vehicle(id=i, profile="driving-car", start=get_shipment_start_point(dt)[::-1],
                              end=get_shipment_end_point(dt)[::-1],
                              capacity=get_capacity(i, nums_of_vehicle),
                              time_window=[Schedule.to_epoch(Schedule.get_shipment_datetime(nums_of_vehicle, i)),
                                           Schedule.to_epoch(Schedule.get_shipment_datetime(nums_of_vehicle, i))])
                      for i in range(nums_of_vehicle)]
    return vehicles


def get_vehicle_number() -> int:
    pattern = r"^([0-9]+)$"
    while True:
        vehicles = input("Input number of vehicle: ")
        if vehicles := re.match(pattern, vehicles):
            if int(vehicles.group(1)) > 0:
                return int(vehicles.group(1))
            print("Number must be grater than 0!")
        print("Input a valid number!")


def get_capacity(index: int, vehicles: int) -> list:
    pattern = r"^([0-9]+)$"
    while True:
        if vehicles > 1:
            capacity = input(f"Input vehicle {index+1} capacity: ")
        else:
            capacity = input(f"Input vehicle capacity: ")
        if capacity := re.match(pattern, capacity):
            if int(capacity.group(1)) > 0:
                return [int(capacity.group(1))]
            print("Number must be grater than 0!")
        print("Input a valid number!")


if __name__ == "__main__":
    main()
