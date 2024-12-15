import pytest
import requests
from faker import Faker
from jsonschema import validate

from utils.pet_api_urls import pet_api_urls
from schemas.pet_api_schemas import pet_schema
from comparison_data.comparison_pets.comparison_pets import pet_single

pets_to_delete_ids = []
fake = Faker()
image_name = "image_for_test_upload.jpg"


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


def test_find_by_status_available_only():
    payload = {
        "status": ["available"]
    }
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["find by status"], params=payload)
    assert r.status_code == 200 and r.json()
    assert [pet for pet in r.json() if pet["status"] == "available"] and \
        not [pet for pet in r.json() if pet["status"] != "available"]


def test_find_by_status_available_and_sold_only():
    payload = {
        "status": ["available", "sold"]
    }
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["find by status"], params=payload)
    assert [pet for pet in r.json() if pet["status"] in ["available", "sold"]] and \
        not [pet for pet in r.json() if pet["status"] not in ["available","sold"]]


def test_check_all_pets_match_schema():
    pets_id_failing_validation = []
    
    payload = {
        "status": ["available", "pending", "sold"]
    }
    
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["find by status"], params=payload)
    for pet in r.json():
        try:
            validate(instance=pet, schema=pet_schema)
        except Exception as e:
            pets_id_failing_validation.append(pet["id"])
    
    assert not pets_id_failing_validation, f"{len(pets_id_failing_validation)} pets do not match the schema: {pets_id_failing_validation}"


def test_get_existing_pet_single():
    pet_id = pet_single["id"]
    r = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet_id))
    assert r.status_code == 200
    assert r.json() == pet_single


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
        "file": open(image_name, "rb")
    }
    r = requests.post(pet_api_urls["domain"] + pet_api_urls["upload image"].format(petId=pet["id"]), files=files)
    assert r.status_code == 200, f"Error in uploading image for pet {pet['id']} - {r.text}"
    
    r_saved = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet["id"]))
    print(r_saved.json())
    assert r_saved.status_code == 200
    if r_saved.status_code == 200 and pet["id"] not in pets_to_delete_ids:
        pets_to_delete_ids.append(pet["id"])


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


def test_delete_existing_pet(post_pet):
    pet, r = post_pet()
    r = requests.delete(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet["id"]))
    assert r.status_code == 200
    
    r_deleted = requests.get(pet_api_urls["domain"] + pet_api_urls["get by petId"].format(petId=pet["id"]))
    assert r_deleted.status_code == 404