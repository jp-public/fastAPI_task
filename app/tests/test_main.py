from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test1_example_values():
    response = client.post('/', json={"cart_value": 790,
                                      "delivery_distance": 2235,
                                      "number_of_items": 4,
                                      "time": "2021-10-12T13:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}


def test2_free_delivery():
    response = client.post('/', json={"cart_value": 10000,
                                      "delivery_distance": 2235,
                                      "number_of_items": 4,
                                      "time": "2021-10-12T13:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 0}


def test3_friday_surge():
    response = client.post('/', json={"cart_value": 790,
                                      "delivery_distance": 2235,
                                      "number_of_items": 4,
                                      "time": "2022-01-28T15:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": int(710*1.1)}


def test4_additional_items():
    response = client.post('/', json={"cart_value": 790,
                                      "delivery_distance": 2235,
                                      "number_of_items": 6,
                                      "time": "2022-01-27T15:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710+50*2}


def test5_fee_cap():
    response = client.post('/', json={"cart_value": 790,
                                      "delivery_distance": 12235,
                                      "number_of_items": 6,
                                      "time": "2022-01-27T15:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 1500}


def test5a_base_distance():
    response = client.post('/', json={"cart_value": 1000,
                                      "delivery_distance": 1000,
                                      "number_of_items": 4,
                                      "time": "2022-01-27T15:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 200}


def test5b_additional_distance_1():
    response = client.post('/', json={"cart_value": 1000,
                                      "delivery_distance": 1001,
                                      "number_of_items": 4,
                                      "time": "2022-01-27T15:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 300}


def test5c_additional_distance_2():
    response = client.post('/', json={"cart_value": 1000,
                                      "delivery_distance": 1500,
                                      "number_of_items": 4,
                                      "time": "2022-01-27T15:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 300}


def test5d_additional_distance_3():
    response = client.post('/', json={"cart_value": 1000,
                                      "delivery_distance": 1501,
                                      "number_of_items": 4,
                                      "time": "2022-01-27T15:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 400}


def test6_min_order():
    response = client.post('/', json={"cart_value": 500,
                                      "delivery_distance": 500,
                                      "number_of_items": 4,
                                      "time": "2022-01-27T15:00:00Z"})
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 200+500}
