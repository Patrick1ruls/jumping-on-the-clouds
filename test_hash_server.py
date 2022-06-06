import json
import os
from urllib import response
import requests
import threading
import subprocess
import time
import pytest


PORT = os.getenv("PORT", "8088")
URL = "http://localhost:" + PORT
HAPPY_PATH_PAYLOAD = {"password": "lion"}


def test_get_stats_data_contract():
    response = requests.request("GET", URL + "/stats")
    response_json = response.json()
    assert response.status_code == 200
    assert "TotalRequests" in response_json
    assert "AverageTime" in response_json
    for key in response_json.keys():
        assert isinstance(response_json.get(key), int)


def test_update_stats():
    first_response = requests.request("GET", URL + "/stats")
    first_total_requests = first_response.json().get("TotalRequests")
    gen_hash()
    second_response = requests.request("GET", URL + "/stats")
    second_total_requests = second_response.json().get("TotalRequests")
    assert second_total_requests > first_total_requests


@pytest.mark.parametrize("payload", [
    {"password": "monkey"},
    {"password": "1234"}, 
    {"password": "-1"}
])
def test_generate_hash_happy_path(payload):
    response = gen_hash(payload=payload)
    assert response.status_code == 200
    assert response.text


@pytest.mark.parametrize("payload", [
    HAPPY_PATH_PAYLOAD,
    {"password": "monkey"},
    {"password": "1234"}, 
    {"password": "-1"}
])
def test_get_hash(payload):
    response = gen_hash(payload=payload)
    id = response.text
    get_response = requests.request("GET", URL + "/hash/" + id)
    print(get_response.text)
    assert get_response.status_code == 200
    assert get_response.text


@pytest.mark.parametrize("payload", [
    {"password": 0},
    {"password": 1234}, 
    {"password": -1}
])
def test_generate_hash_bad_input(payload):
    response = gen_hash(payload=payload)
    assert response.status_code == 400
    assert "Malformed Input" in response.text


@pytest.mark.parametrize(("payload_1", "payload_2"), [
    ({"not_a_password": "a"}, {"not_a_password": "b"}),
    ({"asdfgg": "quiet"}, {"asdbwqqq": "lizard"}),
    ({1088: 56789}, {"not_a_password": "b"}),
    ({"-098765": 87}, {"wishes_it_was_a_password": "oweruhg"})
])
def test_hash_collison(payload_1, payload_2):
    id_1_response = gen_hash({"not_a_password": "a"})
    id_2_response = gen_hash({"not_a_password": "b"})
    get_response_1 = requests.request("GET", URL + "/hash/" + id_1_response.text)
    get_response_2 = requests.request("GET", URL + "/hash/" + id_2_response.text)
    assert get_response_1.text != get_response_2.text, "Hash collision detected"


def test_duplicate_hashes():
    id_1_response = gen_hash()
    id_2_response = gen_hash()
    try:
        assert id_2_response.status_code != 200, "Duplicate request should have failed"
    finally:
        get_response_1 = requests.request("GET", URL + "/hash/" + id_1_response.text)
        get_response_2 = requests.request("GET", URL + "/hash/" + id_2_response.text)
        assert get_response_1.text != get_response_2.text, "Duplicate hash stored in db"


@pytest.mark.parametrize("id", [
    "1234567890",
    "-1",
    "0"
])
def test_get_non_existent_hash(id):
    get_response = requests.request("GET", URL + "/hash/" + id)
    assert get_response.status_code == 400
    assert "Hash not found" in get_response.text


@pytest.mark.parametrize("id", [
    "",
    "v",
    "Random_text"
])
def test_get_error_hash(id):
    get_response = requests.request("GET", URL + "/hash/" + id)
    assert get_response.status_code == 400
    assert "invalid syntax" in get_response.text
    

def gen_hash(payload=HAPPY_PATH_PAYLOAD):
    payload = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json',
    }
    return requests.request("POST", URL + "/hash", headers=headers, data=payload)
