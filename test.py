from datetime import datetime, date, time
import re
from Schedule import Schedule
from pprint import pprint
from tabulate import tabulate


d = {
    "code": 0,
    "summary": {
        "cost": 1109,
        "routes": 2,
        "unassigned": 1,
        "delivery": [184],
        "amount": [184],
        "pickup": [0],
        "setup": 0,
        "service": 5520,
        "duration": 1109,
        "waiting_time": 0,
        "priority": 0,
        "distance": 13798,
        "violations": [],
        "computing_times": {"loading": 29, "solving": 2, "routing": 41},
    },
    "unassigned": [
        {"id": 3, "location": [122.98120235456126, 0.6232849505965705], "type": "job"}
    ],
    "routes": [
        {
            "vehicle": 0,
            "cost": 676,
            "delivery": [95],
            "amount": [95],
            "pickup": [0],
            "setup": 0,
            "service": 2850,
            "duration": 676,
            "waiting_time": 0,
            "priority": 0,
            "distance": 8047,
            "steps": [
                {
                    "type": "start",
                    "location": [123.06570859593717, 0.5314275230046858],
                    "setup": 0,
                    "service": 0,
                    "waiting_time": 0,
                    "load": [95],
                    "arrival": 1709512200,
                    "duration": 0,
                    "violations": [],
                    "distance": 0,
                },
                {
                    "type": "job",
                    "location": [123.06169343367333, 0.5542778527907859],
                    "id": 5,
                    "setup": 0,
                    "service": 900,
                    "waiting_time": 0,
                    "job": 5,
                    "load": [65],
                    "arrival": 1709512412,
                    "duration": 212,
                    "violations": [],
                    "distance": 3319,
                },
                {
                    "type": "job",
                    "location": [123.05288159873872, 0.5466605931932089],
                    "id": 0,
                    "setup": 0,
                    "service": 1200,
                    "waiting_time": 0,
                    "job": 0,
                    "load": [25],
                    "arrival": 1709513532,
                    "duration": 432,
                    "violations": [],
                    "distance": 5125,
                },
                {
                    "type": "job",
                    "location": [123.05629614531824, 0.5441566948534152],
                    "id": 2,
                    "setup": 0,
                    "service": 750,
                    "waiting_time": 0,
                    "job": 2,
                    "load": [0],
                    "arrival": 1709514812,
                    "duration": 512,
                    "violations": [],
                    "distance": 5688,
                },
                {
                    "type": "end",
                    "location": [123.06570859593717, 0.5314275230046858],
                    "setup": 0,
                    "service": 0,
                    "waiting_time": 0,
                    "load": [0],
                    "arrival": 1709515726,
                    "duration": 676,
                    "violations": [],
                    "distance": 8047,
                },
            ],
            "violations": [],
            "geometry": "sxfBcgcnVGCSCCZGd@[nCALQxAi@lEWbCGh@QzAUzBGp@E^WrCCHoBQoF]_BKuAKsCUgF_@IAgIy@qBSOCoGo@kFc@EBI?ECEKoBSkAMqCYsC_@aCSKAmBUaBO]EmBUoLeAm@GOAcBQsAMk@GiAKkEc@kAK]nDQjBEj@QdBwAUoCUw@MGAF@v@LnCTvAT[tCCZKlAEb@YzCWjCMdAQdGGxChAHbFb@nALhJz@tCXxAJlDX~CXR@jALbBP_ApEERGr@EHK@ECCAB@DBJADIFs@DS~@qEjE`@t@L~AgGh@eCj@_Ct@_Dx@cD`@}Ah@uBXkAZoA@ATaAHa@VkAJ[EKBGDCH?DBBD^BjE`@~Gr@xLlAH@fF`@^BrAJ`@DtAJ~AJnF\\nBPVsCD_@Fq@T{BP{AFi@VcCh@mEPyA@MZoCFe@B[RBFB",
        },
        {
            "vehicle": 1,
            "cost": 433,
            "delivery": [89],
            "amount": [89],
            "pickup": [0],
            "setup": 0,
            "service": 2670,
            "duration": 433,
            "waiting_time": 0,
            "priority": 0,
            "distance": 5751,
            "steps": [
                {
                    "type": "start",
                    "location": [123.06570859593717, 0.5314275230046858],
                    "setup": 0,
                    "service": 0,
                    "waiting_time": 0,
                    "load": [89],
                    "arrival": 1709512200,
                    "duration": 0,
                    "violations": [],
                    "distance": 0,
                },
                {
                    "type": "job",
                    "location": [123.05756679993404, 0.5367471519406993],
                    "id": 1,
                    "setup": 0,
                    "service": 900,
                    "waiting_time": 0,
                    "job": 1,
                    "load": [59],
                    "arrival": 1709512328,
                    "duration": 128,
                    "violations": [],
                    "distance": 1584,
                },
                {
                    "type": "job",
                    "location": [123.07636274629743, 0.5405772721723879],
                    "id": 4,
                    "setup": 0,
                    "service": 1770,
                    "waiting_time": 0,
                    "job": 4,
                    "load": [0],
                    "arrival": 1709513395,
                    "duration": 295,
                    "violations": [],
                    "distance": 3840,
                },
                {
                    "type": "end",
                    "location": [123.06570859593717, 0.5314275230046858],
                    "setup": 0,
                    "service": 0,
                    "waiting_time": 0,
                    "load": [0],
                    "arrival": 1709515303,
                    "duration": 433,
                    "violations": [],
                    "distance": 5751,
                },
            ],
            "violations": [],
            "geometry": "sxfBcgcnVGCSCCZGd@[nCALQxAi@lEWbCGh@QzAUzBGp@E^WrCCHoBQoF]_BKuAKsCUgF_@Iv@GHKnAMnA[`CSxChEb@iEc@RyCZaCLoAJoA?KFw@@KZkCDMB[l@mGl@wFT{B?[Ee@Gc@a@gAi@wAm@iBYy@m@_Bc@qAW}@Gg@E_@UmB[wCOcAOeBO}A[gBOs@a@kAUs@{@sBk@oAOa@k@yAM_@wAsDe@cBKe@]gB\\fBJd@d@bBvArDL^j@xAN`@j@nAz@rBTr@`@jANr@ZfBN|ANdBNbAZvCTlBh@WlBaAt@g@PKJALAL@tBn@JBj@PbBh@TFfBh@p@TzCx@|C~@d@NvBn@fCv@Ed@[hCQnAALRBFB",
        },
    ],
}


print(
    "========================================================================================"
)
pprint(d)
print(
    "========================================================================================"
)


def get_summary(result: dict) -> None:
    # print("="*80)
    print(" Routing Result ".center(50, "="))
    headers = ["Summary", "Value"]
    table = [
        ["Planned amount", int(result["summary"]["amount"][0])],
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
        print(f"Route {i+1}".center(50, "-"))
        for i, step in enumerate(route["steps"]):
            type, location, load, arrival, duration, distance, job = (
                step["type"],
                step["location"],
                step["load"],
                datetime.fromtimestamp(step["arrival"]),
                step["duration"],
                step["distance"],
                step.get("job", None)
            )
            if step["type"] == "start":
                print(
                    f"{type.capitalize()}:\tlocation: {location}, load amount: {load[0]}, start time: {arrival}"
                )
            elif step["type"] == "end":
                print(f"{type.capitalize()}:\tlocation: {location}, load amount: {load[0]}, finish time: {arrival}")
            else:
                print(f"{type.capitalize()} {job}:\tlocation: {location}, load amount: {load[0]}, arrival time: {arrival}")


get_summary(d)
