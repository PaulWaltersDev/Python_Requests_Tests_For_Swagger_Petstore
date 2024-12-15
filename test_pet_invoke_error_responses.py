import pytest
import requests
from faker import Faker

from utils.pet_api_urls import pet_api_urls

fake = Faker()

@pytest.fixture()
def post_pet():
    def _post_pet():
        new_pet = {
            "id": fake.random_int(min=1000000000000000000, max=9223372036854775807),
            "category": {
                "id": fake.random_int(min=1, max=9223372036854775807),
                "name": fake.word()
            },
            "name": fake.first_name(),
            "photoUrls": [fake.image_url()],
            "tags": [
                {
                    "id": fake.random_int(min=1, max=9223372036854775807),
                    "name": fake.word()
                }
            ],
            "status": "available"
        }
        
        r = requests.post(pet_api_urls["domain"] + pet_api_urls["pet"], json=new_pet)
        return (new_pet, r)
    return _post_pet


def test_find_by_invalid_status():
    payload = {
        "status": ["invalid_status"]
    }
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["find by status"], params=payload)
    assert r.status_code == 400


def test_find_by_empty_status():
    payload = {
        "status": []
    }
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["find by status"], params=payload)
    assert r.status_code == 400


def test_get_non_existent_pet():
    # At the time of writing this test, the petstore API does not have any pets with id less than 8
    pet_id = 2
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet_id))
    assert r.status_code == 404


def test_get_pet_with_invalid_id():
    pet_id = "not_an_integer"
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet_id))
    assert r.status_code == 400


def test_create_pet_with_non_integer_id():
    incorrect_pet = {
        "id": "not_an_integer",
        "category": {
            "id": fake.random_int(min=1, max=9223372036854775807),
            "name": fake.word()
        },
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "tags": [
            {
                "id": fake.random_int(min=1, max=9223372036854775807),
                "name": fake.word()
            }
        ],
        "status": "available"
    }
    r = requests.post(pet_api_urls["domain"] + pet_api_urls["pet"], json=incorrect_pet)
    assert r.status_code == 405


def test_create_pet_with_negative_id():
    incorrect_pet = {
        "id": -1*fake.random_int(min=1, max=9223372036854775807),
        "category": {
            "id": fake.random_int(min=1, max=9223372036854775807),
            "name": fake.word()
        },
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "tags": [
            {
                "id": fake.random_int(min=1, max=9223372036854775807),
                "name": fake.word()
            }
        ],
        "status": "available"
    }
    r = requests.post(pet_api_urls["domain"] + pet_api_urls["pet"], json=incorrect_pet)
    #assert r.status_code == 405
    
    r_saved = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=incorrect_pet["id"]))
    assert r_saved.status_code == 404


def test_create_pet_with_missing_status():
    incorrect_pet = {
        "id": fake.random_int(min=1, max=9223372036854775807),
        "category": {
            "id": fake.random_int(min=1, max=9223372036854775807),
            "name": fake.word()
        },
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "tags": [
            {
                "id": fake.random_int(min=1, max=9223372036854775807),
                "name": fake.word()
            }
        ]
    }
    r = requests.post(pet_api_urls["domain"] + pet_api_urls["pet"], json=incorrect_pet)
    assert r.status_code == 405


def test_put_non_existent_pet():
    # get pet/findByStatus for all categories shows that at the current time there are no pets with id less than 10000
    incorrect_pet = {
        "id": fake.random_int(min=1, max=10000),
        "category": {
            "id": fake.random_int(min=1, max=9223372036854775807),
            "name": fake.word()
        },
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "tags": [
            {
                "id": fake.random_int(min=1, max=9223372036854775807),
                "name": fake.word()
            }
        ],
        "status": "sold"
    }
    r = requests.put(pet_api_urls["domain"] + pet_api_urls["pet"], json=incorrect_pet)
    assert r.status_code == 404

    
def test_put_pet_with_non_integer_id():
    incorrect_pet = {
        "id": "not_an_integer",
        "category": {
            "id": fake.random_int(min=1, max=9223372036854775807),
            "name": fake.word()
        },
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "tags": [
            {
                "id": fake.random_int(min=1, max=9223372036854775807),
                "name": fake.word()
            }
        ],
        "status": "sold"
    }
    r = requests.put(pet_api_urls["domain"] + pet_api_urls["pet"], json=incorrect_pet)
    assert r.status_code == 400


def test_delete_non_existent_pet():
    # get pet/findByStatus for all categories shows that at the current time there are no pets with id less than 10000    
    nonexistent_pet_id = fake.random_int(min=1, max=10000)
    r = requests.delete(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=nonexistent_pet_id))
    assert r.status_code == 404


def test_delete_pet_with_non_integer_id():
    r = requests.delete(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId="not_an_integer"))
    assert r.status_code == 400