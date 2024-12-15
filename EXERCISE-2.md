# Test Plan

This is a test plan for the implementation of a test automation suite for a subset of API endpoints in the [Swagger Petstore API](https://petstore.swagger.io/).

## Introduction

The plan is to be delivered in two parts -

* API Test Automation suite done in **Python Requests** and **PyTest**
* [Bug Report](BUGREPORT-2.md) containing a list of all found errors with severity.

## In Scope

* In order to save time I have decided to only cover /pet tests. This is because tests for these are sufficient for examples of CRUD, error status codes, invalid data (particularly pet IDs and status) and incorrect or incomplete formats.

## Out of Scope

* Tests for the following /pet endpoints are omitted.
  * ```GET /pet/findByTags``` - the Swagger page has this as deprecated
  * ```POST /post/{petId}``` - Having a parametrized POST endpoint that only updates existing data is dubious and [arguably breaks HTTP/1 standard RFC2616 9.5](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.5) since unlike PUT or (the best choice for this) PATCH, POST is not idempotent and should be used to create new representations only. In a real world project I would probably raise this as a possible API design bug (see [Bug List](BUGREPORT-1.md)) and only if it's approved, write tests for it.
* Performance (including Load and Stress) Tests
* Devoted Security / Pentesting

## Implementation and Resources

* The API Test Automation suite will be done using **Requests** in Python 3 and **Pytest*** for the assertion framework. This is not my usual tooling but apparently already familiar to the assessing team, which should make it easier for them to deploy, understand and judge them against other submissions and their own expectations.

* For other technical considerations check out the [Test Suite](TEST_SUITE.md) page.

## Timeframe

To be done from Fri 13th Dec - Sun 15th Dec 2024

## Deliverables

* API Test Suite corresponding to the above scope.
* Report Showing Passed and Failed Tests
* List of Raised Bugs

## Risks

* Incapacity, illness or other impact to the human resource
* Outage of the https://petstore.swagger.io/v2 API
* Damage to Paul's computer or Dev environment
