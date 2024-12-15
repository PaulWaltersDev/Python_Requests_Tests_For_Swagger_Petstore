# Python_Requests_Tests_For_Swagger_Petstore
A Set of Tests Written in Python and Using Requests and PyTest against the pet endpoints of the [Pet Store Swagger API](https://petstore.swagger.io/).

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

There is one set of tests along with a page objects folder and conftest.py file in the suite within src/tests.

```
src/tests/test_pet_search_CRUD.py
```

It can be run via the command -

```
pytest src/tests/test_pet_search_CRUD.py
```

## Bug Report

The list of bugs raised via the above can be found [here](BUGREPORT-2.md)
