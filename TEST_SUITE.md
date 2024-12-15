# Test Suite and Architecture

This details the test code itself, the architectural approach and reasons for specific decisions.

## Focus and Scope

As stated in the [Test Plan](EXERCISE-2.md) these tests focus on a subset of the Pet Store API - those related to the /pet set of endpoint and functionalities with a few omissions.

In doing so I have covered the following types of scenarios -

* Basic Create/Read/Update/Delete (CRUD) Pet request scenarios
* Requests with invalid IDs and Status designed to invoke error response codes as set out in the [swagger document](https://petstore.swagger.io/#/)
* Validation of all returned pets against the schema set out in ```GET /pet/findByStatus``` Code 200 (Successful Operation) of the swagger document.

For Pet creation, update and deletion, each test includes a ```GET /pet/{pet_id}``` request and additional assertions to retrieve the pet in question and compare against expected.

## Tooling

All work was done in Ubuntu Linux on Visual Studio Code with Github Copilot, OpenAI GPT 4o. Copilot code generation was only used prodigiously in this case to generate the new_pet dictionary in fixture ```def post_pet()```.

## Architectural Implementation.

### Test Design

These tests are designed to be atomic and self-contained. For example, a test to update (PUT) or delete a pet includes a previous call to the fixture ```def post_pet()``` to POST and retrieve a new created pet dictionary first.

However for tests in ```test_pet_invoke_error_messages.py``` where all CRUD operations are expected to fail with error codes the creation of a pet dictionary in included in the tes and not done via fixture. This is deliberate and is done to make it look obvious to a reader what invalid valid is added and where.

### Test Files

Tests involving happy path CRUD and validation and those invoking error responses have been separated into two different files in the root folder in order to make them easier to navigate and study -

```
test_pet_invoke_error_responses.py
test_pet_search_CRUD.py
```

### Supporting Files

The paths to endpoints covered in the test is separated from each test file and stored in a dictionary in utils/pet_api_urls.py. This is so that they can be (if necessary) amended without having to touch the test files themselves.

Supporting data objects such as the Pet API Schema (used to validate the schema of all pets retrieved from ```GET /pet/findByStatus```)  and Comparison Pet (used to compare against the output of ```GET /pet``` for a specific pre-selected pet) are also stored in files in their own subfolders and called as modules.

A specimen image for file upload is stored in the root folder.

Other modules used are -
* ```Faker``` to generate fake test data used in most tests
* ```jsonschema``` to validate the Pet schema

### Use of Assertions

Usually I only use one or two assertions in a test however some happy path CRUD tests - notably PUT and DELETE - have more. This is to check that the initial pet creation, a prerequisite for these tests, was completed successfully before proceeding to PUT or DELETE.

Obviously this means that testing PUT and DELETE are contingent on a previous ```POST /pet``` working as expected, however the only alternative is to pick an existing pet ID and use that instead, which makes the test on such an open api especially brittle and reliant on that pet not being deleted by another user.

### Comments and DocStrings

I have put comments to explain the reasoning for certain implementations I have done. However I believe the test names I have chosen are simple and obvious enough, so have not felt the need this time (unlike in the Selenium project for instance) to include DocStrings for each test.

### Cleanup

For tests in ```test_pet_search_CRUD.py``` the fixture ```def delete_created_pets()``` with modular scope is run to ieratively delete all pets expected to have been created in previous tests in the module. This is so that in the case of working-as-expected API requests the Petstore is left as one found it.
