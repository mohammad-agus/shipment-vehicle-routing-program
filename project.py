import folium
from openrouteservice.optimization import Job, Vehicle
from openrouteservice import Client, convert
import re
import csv
from typing import Union
from datetime import datetime, date, time
from Schedule import Schedule
from tabulate import tabulate

# Load API key
from dotenv import dotenv_values

api_key = dotenv_values(".env")["API_KEY"]


def main():

    data: list = get_csv_data()
    client = Client(key=api_key)
    route_map = folium.Map(
        location=get_shipment_start_point(data), tiles="openstreetmap", zoom_start=14
    )

    folium.Marker(
        location=get_shipment_start_point(data), icon=folium.Icon(color="red")
    ).add_to(route_map)
    for coord in get_shipment_points(data):
        folium.Marker(location=coord).add_to(route_map)

    jobs = []
    for i, loc in enumerate(get_job_list(data)):
        jobs.append(
            Job(
                id=i,
                location=loc["location"][::-1],
                amount=loc["amount"],
                service=loc["service"],
            )
        )

    number_of_vehicles = get_vehicle_number()
    vehicles = get_vehicles(data, number_of_vehicles)
    optimized = client.optimization(jobs=jobs, vehicles=vehicles, geometry=True)
    for route in optimized["routes"]:
        folium.PolyLine(
            locations=[
                route[::-1]
                for route in convert.decode_polyline(route["geometry"])["coordinates"]
            ]
        ).add_to(route_map)

    get_summary(result=optimized, source=data)
    route_map.save("route_map.html")


def get_coord(location: dict) -> list:
    return [location["lat"], location["long"]]


def get_shipment_points(dt: list) -> list:
    return [[loc["lat"], loc["long"]] for loc in dt[2:]]


def get_shipment_start_point(dt: list) -> list:
    return [dt[0]["lat"], dt[0]["long"]]


def get_shipment_end_point(dt: list) -> list:
    return [dt[1]["lat"], dt[1]["long"]]


def get_job_list(dt: list) -> list[dict]:
    return [
        {
            "location": [job["lat"], job["long"]],
            "amount": job["delivery_amount"],
            "service": job["service"],
        }
        for job in dt[2:]
    ]


def get_job_index(dt: list) -> list:
    return [i.get("id") for i in dt[2:]]


def get_csv_data() -> list[dict]:
    while True:
        try:
            file_path = input("Input csv file: ")
            with open(file_path) as input_data:
                dt = csv.DictReader(input_data)
                return [
                    {
                        "id": row["id"],
                        "lat": float(row["lat"]),
                        "long": float(row["long"]),
                        "delivery_amount": [int(row["delivery_amount"])],
                        "service": int(row["service"]),
                    }
                    for row in dt
                ]
        except FileNotFoundError:
            print("Please input a valid csv file!")
            pass


def get_vehicles(dt, nums_of_vehicle) -> list:
    vehicles: list = [
        Vehicle(
            id=i,
            profile="driving-car",
            start=get_shipment_start_point(dt)[::-1],
            end=get_shipment_end_point(dt)[::-1],
            capacity=get_capacity(vehicles=nums_of_vehicle, index=i),
            time_window=Schedule.get_vehicle_time_window(
                vehicles=nums_of_vehicle,
                idx=i,
                datetime_to_epoch_function=Schedule.to_unix_timestamp,
            ),
        )
        for i in range(nums_of_vehicle)
    ]
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


def get_capacity(vehicles: int, index: int) -> list:
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


def get_planned_amount(jobs: dict) -> int:
    amount = [job["amount"][0] for job in jobs]
    return sum(amount)


def get_summary(result: dict, source: dict) -> None:
    # print("="*80)
    print(" Routing Result ".center(50, "="))
    headers = ["Summary", "Value"]
    table = [
        ["Planned amount", get_planned_amount(get_job_list(source))],
        ["Delivery amount", result["summary"]["delivery"][0]],
        ["Routes", result["summary"]["routes"]],
        [
            "Distance",
            f'{result["summary"]["distance"]} meters ({result["summary"]["distance"]/1000:.2f} km)',
        ],
        [
            "Duration",
            f'{result["summary"]["duration"]} seconds ({result["summary"]["duration"]/60:.2f} minutes)',
        ],
        ["Unassigned", result["summary"]["unassigned"]],
    ]
    print(
        tabulate(
            headers=headers, tabular_data=table, tablefmt="psql", disable_numparse=True
        )
    )
    for i, route in enumerate(result["routes"]):
        print(f"Route {i+1}: Vehicle {route['vehicle']}".center(50, "-"))
        for i, step in enumerate(route["steps"]):
            type, location, load, arrival, duration, distance, job = (
                step["type"],
                step["location"],
                step["load"],
                datetime.fromtimestamp(step["arrival"]),
                step["duration"],
                step["distance"],
                step.get("job", None),
            )
            if step["type"] == "start":
                print(
                    f"{type.capitalize()}:\t {location}, load amount: {load[0]}, start time: {arrival}"
                )
            elif step["type"] == "end":
                print(
                    f"{type.capitalize()}:\t {location}, load amount: {load[0]}, finish time: {arrival}"
                )
            else:
                print(
                    f"{type.capitalize()} {job+1}:\t {location}, load amount: {load[0]}, arrival time: {arrival}"
                )


if __name__ == "__main__":
    main()
