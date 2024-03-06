import csv
import folium
import re
import math
from datetime import datetime
from dotenv import dotenv_values
from openrouteservice import Client, convert
from openrouteservice.optimization import Job, Vehicle
from tabulate import tabulate

# Load API key
api_key = dotenv_values(".env")["API_KEY"]


class Schedule:

    @classmethod
    def to_unix_timestamp(cls, date_time: datetime) -> datetime.timestamp:
        return date_time.timestamp()

    @classmethod
    def get_vehicle_time_window(
        cls, vehicles: int, idx: int, datetime_to_epoch_function
    ) -> list[datetime]:
        p = r"^(2[0-9]{3})-0?([1-9]|1[0-2])-0?([1-9]|[1-3][0-9]) 0?([1-9]|[1-2][0-9]):0?([0-9]|[1-5][0-9])$"
        while True:
            try:
                print('Date and time format: "YYYY-MM-DD HH:mm"')
                if vehicles > 1:
                    print(
                        f"Input shipment schedule (date & time) of vehicle {idx+1} (in  format):"
                    )
                else:
                    print(
                        'Input shipment schedule (date & time) of the vehicle in "YYYY-MM-DD HH:mm" format:'
                    )
                dt1 = input(f"Begin: ")
                dt1 = re.match(pattern=p, string=dt1)
                if dt1 is None:
                    print("Please input a valid datetime!")
                    continue
                ts1 = datetime(
                    int(dt1.group(1)),
                    int(dt1.group(2)),
                    int(dt1.group(3)),
                    int(dt1.group(4)),
                    int(dt1.group(5)),
                    0,
                )
                dt2 = input(f"End: ")
                dt2 = re.match(pattern=p, string=dt2)
                if dt2 is None:
                    print("Please input a valid datetime!")
                    continue
                ts2 = datetime(
                    int(dt2.group(1)),
                    int(dt2.group(2)),
                    int(dt2.group(3)),
                    int(dt2.group(4)),
                    int(dt2.group(5)),
                    0,
                )
                if ts1 >= ts2:
                    print("Invalid input: datetime beginning >= datetime ending!")
                    continue
                return [
                    datetime_to_epoch_function(ts1),
                    datetime_to_epoch_function(ts2),
                ]
            except ValueError:
                print("Please input a valid datetime!")
                pass


class Color:

    colors = [
        "red",
        "blue",
        "green",
        "purple",
        "orange",
        "darkred",
        "lightred",
        "beige",
        "darkblue",
        "darkgreen",
        "cadetblue",
        "darkpurple",
        "white",
        "pink",
        "lightblue",
        "lightgreen",
        "gray",
        "black",
        "lightgray",
    ]

    @classmethod
    def get_colors(cls, n: int) -> list:
        return cls.colors * n


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

    jobs = [
        Job(
            id=i,
            location=loc["location"][::-1],
            amount=loc["amount"],
            service=loc["service"],
        )
        for i, loc in enumerate(get_job_list(data))
    ]

    number_of_vehicles = get_vehicle_number()
    vehicles = get_vehicles(data, number_of_vehicles)
    optimized = client.optimization(jobs=jobs, vehicles=vehicles, geometry=True)
    
    colors = Color.get_colors(n=math.ceil(len(optimized["routes"]) / len(Color.colors)))
    for i, route in enumerate(optimized["routes"]):
        folium.PolyLine(
            locations=[
                route[::-1]
                for route in convert.decode_polyline(route["geometry"])["coordinates"]
            ],
            color=colors[route["vehicle"]],
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


def get_planned_amount(jobs: list[dict]) -> int:
    amount = [job["amount"][0] for job in jobs]
    return sum(amount)


def get_summary(result: dict, source: list[dict]) -> None:
    # print("="*80)
    print("\nSummary:")
    headers = ["Result", "Value"]
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
    for idx, route in enumerate(result["routes"]):
        print(f"\n>> Route {idx+1}: Vehicle {route['vehicle']+1} ")
        for i, step in enumerate(route["steps"]):
            job_type, location, load, arrival, duration, distance, job_id = (
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
                    f"{job_type.capitalize()}:\t{location}, load amount: {load[0]}, start time: {arrival}"
                )
            elif step["type"] == "end":
                print(
                    f"{job_type.capitalize()}:\t{location}, load amount: {load[0]}, finish time: {arrival}"
                )
            else:
                print(
                    f"{job_type.capitalize()} {job_id+1}:\t{location}, load amount: {load[0]}, arrival time: {arrival}"
                )
    print(f"\nUnassigned:")
    for job in result["unassigned"]:
        job_id = job["id"]
        location = job["location"]
        amount = get_job_list(source)[job_id].get("amount")[0]
        print(f"Job {job_id+1}:\t{location}, amount: {amount}")


def get_colors(len_route: int) -> list:
    colors = [
        "red",
        "blue",
        "green",
        "purple",
        "orange",
        "darkred",
        "lightred",
        "beige",
        "darkblue",
        "darkgreen",
        "cadetblue",
        "darkpurple",
        "white",
        "pink",
        "lightblue",
        "lightgreen",
        "gray",
        "black",
        "lightgray",
    ]
    if len_route > len(colors):
        return round(len_route / len(colors)) * colors


if __name__ == "__main__":
    main()
