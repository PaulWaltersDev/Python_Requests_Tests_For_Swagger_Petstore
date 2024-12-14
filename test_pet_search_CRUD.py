import pytest
import requests
import json
from faker import Faker
from jsonschema import validate

from schemas.pet_api_schemas import pet_schema
from comparison_data.comparison_pets.comparison_pets import pet_single

pets_to_delete_ids = []
fake = Faker()

pet_api_urls = {
    "domain" : "https://petstore.swagger.io/v2/",
    "find by status" : "pet/findByStatus",
    "pet" : "pet",
    "upload image" : "pet/{petId}/uploadImage",
    "get by petId" : "pet/{petId}"
}

@pytest.fixture(scope="module", autouse=True)
def delete_created_pets():
    yield
    for pet_id in pets_to_delete_ids:
        r = requests.delete(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet_id))
        assert r.status_code == 200, f"Error in deleting pet with id {pet_id}"

@pytest.fixture()
def post_pet():
    def _post_pet():
        new_pet = {
            "id": fake.random_int(min=10000000, max=9223372036854775807),
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

def test_find_by_status_available_only():
    payload = {
        "status": ["available"]
    }
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["find by status"], params=payload)
    assert r.status_code == 200 and r.json()
    assert [pet for pet in r.json() if pet["status"] == "available"]
    assert not [pet for pet in r.json() if pet["status"] != "available"]

def test_find_by_status_available_and_sold_only():
    payload = {
        "status": ["available", "sold"]
    }
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["find by status"], params=payload)
    assert r.status_code == 200 and r.json()
    assert [pet for pet in r.json() if pet["status"] in ["available", "sold"]]
    assert not [pet for pet in r.json() if pet["status"] not in ["available","sold"]]
    for pet in r.json():
        try:
            validate(instance=pet, schema=pet_schema)
        except Exception as e:
            assert False, f"Error in validating pet {pet['id']}: {e}"

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

def test_get_existing_pet_single():
    pet_id = 9223372016900014281
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet_id))
    assert r.status_code == 200
    assert r.json() == pet_single
    validate(instance=r.json(), schema=pet_schema)

def test_get_non_existent_pet():
    pet_id = 1000
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet_id))
    assert r.status_code == 404

def test_get_pet_with_invalid_id():
    pet_id = "not_an_integer"
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet_id))
    assert r.status_code == 400

def test_create_pet(post_pet):
    pet, r = post_pet()
    assert r.status_code == 200
    assert r.json() == pet
    validate(instance=r.json(), schema=pet_schema)
    
    r_saved = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet["id"]))
    assert r_saved.status_code == 200
    assert r_saved.json() == pet
    if r_saved.status_code == 200 and pet["id"] not in pets_to_delete_ids:
        pets_to_delete_ids.append(pet["id"])

def test_create_pet_and_upload_image(post_pet):
    pet, r = post_pet()
    files = {
        "file": open("image_for_test_upload.jpg", "rb")
    }
    r = requests.post(pet_api_urls["domain"] + pet_api_urls["upload image"].format(petId=pet["id"]), files=files)
    assert r.status_code == 200, f"Error in uploading image for pet {pet['id']} - {r.text}"
    
    r_saved = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet["id"]))
    assert r_saved.status_code == 200
    assert r_saved.json() == pet
    if r_saved.status_code == 200 and pet["id"] not in pets_to_delete_ids:
        pets_to_delete_ids.append(pet["id"])
    
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
    assert r.status_code == 405
    
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

def test_put_existing_pet(post_pet):
    pet, r = post_pet() 
    
    pet["name"] = fake.first_name()
    pet["status"] = "sold"
    r = requests.put(pet_api_urls["domain"] + pet_api_urls["pet"], json=pet)
    assert r.status_code == 200
    assert r.json() == pet
    validate(instance=r.json(), schema=pet_schema)
    
    r_saved = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet["id"]))
    assert r_saved.status_code == 200
    assert r_saved.json() == pet


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

def test_delete_existing_pet(post_pet):
    pet, r = post_pet()
    r = requests.delete(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet["id"]))
    assert r.status_code == 200
    
    r_deleted = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet["id"]))
    assert r_deleted.status_code == 404

def test_delete_non_existent_pet():
    # get pet/findByStatus for all categories shows that at the current time there are no pets with id less than 10000    
    nonexistent_pet_id = fake.random_int(min=1, max=10000)
    r = requests.delete(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=nonexistent_pet_id))
    assert r.status_code == 404

def test_delete_pet_with_non_integer_id():
    r = requests.delete(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId="not_an_integer"))
    assert r.status_code == 400

