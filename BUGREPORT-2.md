### Bug Report

### Notes

* I have specified severities (Low, Medium, High - high being stopping some important action or a 200 Response (suggesting creation or update of a pet) that should not have been. I have not specified priorities though, considering in most companies that would be done by someone with power/influence over the dev team i.e. a stakeholder, project manager or dev lead.

## Tests - ```test_pet_search_CRUD.py```

```
================================ short test summary info =================================
FAILED test_pet_search_CRUD.py::test_check_all_pets_match_schema - AssertionError: 31 pets do not match the schema: [9223372016900012561, 92233720169000...
============================== 1 failed, 7 passed in 24.20s ==============================

Later run (see AUTO-PET-03)

================================ short test summary info =================================
FAILED test_pet_search_CRUD.py::test_check_all_pets_match_schema - AssertionError: 15 pets do not match the schema: [9223372016900012781, 92233720169000...
FAILED test_pet_search_CRUD.py::test_get_existing_pet_single - assert 404 == 200
============================== 2 failed, 6 passed in 26.97s ==============================
```

| Bug ID  | Description | Found in Test | Severity |
| --- | --- | --- | --- |
| AUTO-PET-01 | Pet Items found not conforming to 200 OK schema for ```GET pet/findByStatus``` | test_check_all_pets_match_schema |  Medium/High, suggests data cleanup required |
| AUTO-PET-02 | Request ```POST /pet/{pet_id}``` for updating existing Pets is a bad use of POST and breaks HTTP/1 standards. It should really be a PATCH request. | N/A |  Medium, does not break any current actions but allows for uncertain behaviour |
| *AUTO-PET-03 | Previously known existing pets retrievable via ```GET pet/{pet_id} no longer retrievable later under same pet ID. Demonstrated with (among others) pet_id "9223372016900012624" | test_get_existing_pet_single |  High |

*See links to screenshots below.

* Whilst Retrievable
[From Browser](https://drive.google.com/file/d/1tYGAEv4ILZy8qEIIUuDxK7RsXKrdRUB4/view?usp=sharing)
[Test Passing](https://drive.google.com/file/d/1tfJWHkzGpeuB7B1jiMICQc8hll0zGYer/view?usp=sharing)

* When Later Not Retrievable
[From Browser](https://drive.google.com/file/d/1myyEBomD-O8Fi3kDEThkfevIk9wi-iec/view?usp=sharing)
[Test Failing](https://drive.google.com/file/d/1UMW_3tuw053e5EuLihuOTyKt82ACfdkZ/view?usp=sharing)

## Tests - ```test_pet_invoke_error_responses.py```

```
================================ short test summary info =================================
FAILED test_pet_invoke_error_responses.py::test_find_by_invalid_status - assert 200 == 400
FAILED test_pet_invoke_error_responses.py::test_find_by_empty_status - assert 200 == 400
FAILED test_pet_invoke_error_responses.py::test_get_pet_with_invalid_id - assert 404 == 400
FAILED test_pet_invoke_error_responses.py::test_create_pet_with_non_integer_id - assert 500 == 405
FAILED test_pet_invoke_error_responses.py::test_create_pet_with_negative_id - assert 200 == 405
FAILED test_pet_invoke_error_responses.py::test_create_pet_with_missing_status - assert 200 == 405
FAILED test_pet_invoke_error_responses.py::test_update_non_existent_pet - assert 200 == 404
FAILED test_pet_invoke_error_responses.py::test_update_pet_with_non_integer_id - assert 500 == 400
FAILED test_pet_invoke_error_responses.py::test_delete_pet_with_non_integer_id - assert 404 == 400
============================== 9 failed, 2 passed in 12.50s ==============================
```

| Bug ID  | Description | Found in Test | Severity |
| --- | --- | --- | --- |
| AUTO-PET-04 | ```GET pet/findByStatus``` for an empty status "" returns 200 OK. The expected response code from the swagger doc is 400| test_find_by_invalid_status |  Medium - not good but no change of state or data |
| AUTO-PET-05 | ```GET pet/findByStatus``` for an invalid status "invalid status" returns 200 OK. The expected response code from the swagger doc is 400| test_find_by_empty_status |  Medium - not good but no change of state or data |
| AUTO-PET-06 | ```GET pet/{pet_id}``` for an invalid id "not an integer" returns 200 OK. The expected response code from the swagger doc is 400| test_get_pet_with_invalid_id |  Medium - not good but no change of state or data |
| AUTO-PET-07 | ```POST pet``` with pet with invalid id "not an integer" returns 500 (Internal Server Error). The expected response code from the swagger doc is 405| test_create_pet_with_non_integer_id |  Medium/High |
| AUTO-PET-08 | ```POST pet``` with pet with negative id returns 200 OK. Negative ids are not likely to be valid and the expected response code from the swagger doc is 405| test_create_pet_with_negative_id |  High - pet with negative ID is likely to be created |
| AUTO-PET-09 | ```POST pet``` with pet with missing status field returns 200 OK. The expected response code from the swagger doc is 405| create_pet_with_missing_status |  High - if this continues then it will just allow for more pets to be added that don't confirm to the stated schema (see AUTO-PET-01) and thus lower data quality overall |
| AUTO-PET-10 | ```PUT pet``` with non-existent pet ID returns 200 OK. The expected response code from the swagger doc is 404| test_update_non_existent_pet |  High - Pet probably created as new record |
| AUTO-PET-11 | ```PUT pet``` with invalid ID "not an integer" returns 500. The expected response code from the swagger doc is 400| test_update_pet_with_non_integer_id |  Medium/High |
| AUTO-PET-12 | ```DELETE pet/{pet_id}``` with invalid ID "not an integer" returns 404. The expected response code from the swagger doc is 400| test_delete_pet_with_non_integer_id |  Low/Medium - Not confirming to the doc but largely inconsequential |
