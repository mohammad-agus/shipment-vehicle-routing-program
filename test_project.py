from project import (
    get_shipment_start_point,
    get_shipment_end_point,
    get_job_list,
    get_job_index,
)


source = [
    {
        "id": "start",
        "lat": 0.5705953948161725,
        "long": 123.05911896076756,
        "delivery_amount": 0,
        "service": 0,
    },
    {
        "id": "end",
        "lat": 0.5461229144422185,
        "long": 123.07928098393106,
        "delivery_amount": 0,
        "service": 0,
    },
    {
        "id": "point01",
        "lat": 0.5631471392390268,
        "long": 123.05288470178134,
        "delivery_amount": 40,
        "service": 1200,
    },
    {
        "id": "point02",
        "lat": 0.5593274803137437,
        "long": 123.06239670199969,
        "delivery_amount": 30,
        "service": 900,
    },
    {
        "id": "point03",
        "lat": 0.5421563811124765,
        "long": 123.08181070778429,
        "delivery_amount": 25,
        "service": 750,
    },
]


def test_get_shipment_start_point():
    assert get_shipment_start_point(source) == [0.5705953948161725, 123.05911896076756]


def test_get_shipment_end_point():
    assert get_shipment_end_point(source) == [0.5461229144422185, 123.07928098393106]


def test_def_get_job_list():
    assert get_job_list(source) == [
        {
            "location": [0.5631471392390268, 123.05288470178134],
            "amount": 40,
            "service": 1200,
        },
        {
            "location": [0.5593274803137437, 123.06239670199969],
            "amount": 30,
            "service": 900,
        },
        {
            "location": [0.5421563811124765, 123.08181070778429],
            "amount": 25,
            "service": 750,
        },
    ]


def test_get_job_index():
    assert get_job_index(source) == ["point01", "point02", "point03"]
