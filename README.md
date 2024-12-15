# Python Requests Tests For Petstore
A Set of Tests Written in Python and Using Requests and PyTest against the pet endpoints and request methods of the [Pet Store API](https://petstore.swagger.io/).

## Test Plan and Implementation Details

I invite you to study the [test plan](EXERCISE-2.md) and [API Test Code Implementation Details](TEST_SUITE.md) for the above.

## Deployment Instructions

1. For Your environment ensure you have the latest [Python3](https://www.python.org/downloads/) installed. This project was written using python3.12.
2. "git clone" this repository into a folder.
3. Navigate to the folder the repo is in and [create and activate a new venv environment](https://realpython.com/python-virtual-environments-a-primer/#create-it).

For example in ubuntu linux this can be done via -

```
python3 -m venv .testvenv (or any name you wish)
source .testvenv/bin/activate
```

You should now see in your terminal something like -

```
(.testvenv) (user)@Ubuntu:~/(folderpath)/Python_Requests_Tests_For_Swagger_Petstore$

```
4. A requirements file stating the correct python modules and components needed for these tests, requirements.txt, was also included. You can run this and install all required components via -

```
pip install -r requirements.txt
```

##Execution Instructions

There are two sets of tests in the suite.

```
test_pet_search_CRUD.py
test_pet_invoke_error_responses.py
```

They can be run via the command -

```
pytest test_pet_search_CRUD.py
pytest test_pet_invoke_error_responses.py
```

With the current state of the API and set set of bugs (see bottom) you will see an output like -

```
# for test_pet_search_CRUD.py

=========================== short test summary info ============================
FAILED test_pet_search_CRUD.py::test_check_all_pets_match_schema - AssertionError: 2 pets do not match the schema: [9223372036854775048, 92233...
FAILED test_pet_search_CRUD.py::test_get_existing_pet_single - assert 404 == 200
========================= 2 failed, 6 passed in 40.17s =========================

# for test_pet_invoke_error_responses.py

=========================== short test summary info ============================
FAILED test_pet_invoke_error_responses.py::test_find_by_invalid_status - assert 200 == 400
FAILED test_pet_invoke_error_responses.py::test_find_by_empty_status - assert 200 == 400
FAILED test_pet_invoke_error_responses.py::test_get_pet_with_invalid_id - assert 404 == 400
FAILED test_pet_invoke_error_responses.py::test_create_pet_with_non_integer_id - assert 500 == 405
FAILED test_pet_invoke_error_responses.py::test_create_pet_with_negative_id - assert 200 == 405
FAILED test_pet_invoke_error_responses.py::test_create_pet_with_missing_status - assert 200 == 405
FAILED test_pet_invoke_error_responses.py::test_update_non_existent_pet - assert 200 == 404
FAILED test_pet_invoke_error_responses.py::test_update_pet_with_non_integer_id - assert 500 == 400
FAILED test_pet_invoke_error_responses.py::test_delete_pet_with_non_integer_id - assert 404 == 400
========================= 9 failed, 2 passed in 15.21s =========================

```

## Bug Report

The list of bugs raised via the above can be found [here](BUGREPORT-2.md)
