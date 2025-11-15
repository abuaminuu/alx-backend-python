
# 🧪 Unit Testing — `test_utils.py`

## Overview

The `test_utils.py` module contains a comprehensive suite of **unit tests** for validating the behavior of utility functions defined in `utils.py`. These tests are written using Python’s built-in **`unittest`** framework and enhanced with the **`parameterized`** library to enable reusable, data-driven testing.

The primary focus of this test suite is the `access_nested_map` function, which retrieves values from nested dictionary structures using tuple-based key paths. This function is critical for ensuring safe and predictable data access patterns across backend modules.

## Key Features

* **Parameterized Testing:** Tests multiple input combinations efficiently using `@parameterized.expand`.
* **Positive Test Cases:** Verifies correct return values for valid dictionary-path combinations.
* **Negative Test Cases:** Confirms that `KeyError` is properly raised when invalid keys are accessed.
* **Strict Compliance:** All functions, classes, and modules include docstrings and type annotations to meet ALX Python documentation standards.

## Learning Outcomes

This test reinforces best practices in:

* Unit testing with `unittest`
* Data-driven testing using `parameterized`
* Writing clean, maintainable, and well-documented test code

By ensuring correctness and stability of `utils.py`, this module contributes to building **robust, production-grade backend systems**.

---
Here’s an updated **`README.md`** section that includes both **Task 0** and **Task 1** — reflecting the work you’ve done on `test_utils.py` with clear documentation and professional tone for GitHub or LinkedIn sharing 👇

---

# 🧪 Unit Testing — `test_utils.py`

## Overview

This module contains unit tests for the `utils.access_nested_map` function. The goal of this exercise is to deepen understanding of **Python’s unittest framework**, **parameterized testing**, and **exception handling**. The tests validate both correct outputs and proper error handling behavior of the utility function.

---

## 🧩 Task 0 — Parameterize a Unit Test

**Objective:**
Write tests that ensure `access_nested_map()` correctly returns values from nested dictionaries based on the provided key path.

**Implementation Highlights:**

* Created `TestAccessNestedMap` class inheriting from `unittest.TestCase`.
* Used `@parameterized.expand` to test multiple input combinations in a concise, DRY approach.
* Verified function output using `assertEqual()`.

**Example Cases:**

```python
({"a": 1}, ("a",), 1)
({"a": {"b": 2}}, ("a",), {"b": 2})
({"a": {"b": 2}}, ("a", "b"), 2)
```

---

## ⚙️ Task 1 — Test Exception Handling with Parameterization

**Objective:**
Ensure that `access_nested_map()` raises `KeyError` when accessing invalid or missing keys.

**Implementation Highlights:**

* Added `test_access_nested_map_exception()` using `assertRaises` context manager.
* Used `@parameterized.expand` for multiple failing scenarios.
* Validated the correctness of the `KeyError` message using `repr(path[-1])`.

**Example Cases:**

```python
({}, ("a",))
({"a": 1}, ("a", "b"))
```

---

## 🧠 Key Learnings

* How to **parameterize test inputs** to improve code coverage efficiently.
* How to use **context managers (`assertRaises`)** for precise exception testing.
* Importance of **verifying exception messages** to ensure correctness and clarity.
* Reinforced best practices for **test readability**, **type annotations**, and **docstring documentation**.

---

Would you like me to extend this README with a short “Project Reflection / Challenges & Breakthroughs” section (like your brag list format for LinkedIn)? It would summarize what you learned and overcame in this testing challenge.
Here’s a polished **README for `test_utils.py`** covering Tasks 0–2, including the unit tests for `access_nested_map` and `get_json`:

---

# `test_utils.py`

This module contains unit tests for utility functions in the `utils` package. It ensures correctness, error handling, and proper external behavior simulation using Python’s `unittest` framework, `parameterized` testing, and `unittest.mock`.

## Tested Functions

### 1. `access_nested_map(nested_map: dict, path: tuple) -> any`

* **Purpose:** Safely access values in a nested dictionary following the sequence of keys in `path`.
* **Tests:**

  * `TestAccessNestedMap.test_access_nested_map`

    * Validates that the function returns the correct value for multiple nested paths using `@parameterized.expand`.
  * `TestAccessNestedMap.test_access_nested_map_exception`

    * Ensures that a `KeyError` is raised when attempting to access a non-existent key.
    * Checks that the exception message correctly reflects the missing key.

### 2. `get_json(url: str) -> dict`

* **Purpose:** Perform an HTTP GET request and return the JSON response.
* **Tests:**

  * `TestGetJson.test_get_json`

    * Mocks `requests.get` to avoid real HTTP calls.
    * Ensures that `get_json` returns the expected payload for different URLs.
    * Verifies that the `requests.get` method is called exactly once with the correct URL.

## Key Features

* Uses `parameterized.expand` to test multiple inputs concisely.
* Uses `unittest.mock.patch` to isolate tests from external dependencies.
* Full **type annotations** and **docstrings** are provided for all classes and methods.
* Exception handling and output verification are explicitly tested to ensure robust utility functions.

## Running Tests

```bash
python3 -m unittest discover -s tests
```

This module is part of a larger project focused on building reliable, well-tested Python utility functions for backend applications.

---

If you want, I can **also draft a short LinkedIn-friendly “skills & achievements” post** based on this testing project, highlighting challenges and breakthroughs. Do you want me to do that next?

# ALL
Perfect — here’s a **polished, submission-ready `README.md`** for your `0x03-Unittests_and_integration_tests` project.
It covers **all 10 tasks**, from unit testing through integration testing, in a clean and professional style suitable for your ALX GitHub repo 👇

---

# 🧪 0x03. Unittests and Integration Tests

This project focuses on **unit testing and integration testing** in Python — ensuring code correctness, reliability, and maintainability.
It’s part of the **ALX Backend Python** track and applies testing concepts to real-world scenarios involving API clients and utility functions.

---

## 📚 Learning Objectives

By completing this project, you will be able to:

* Write **unit tests** using `unittest` and `parameterized`
* Use **mocking** to simulate HTTP requests and dependencies
* Test for **exceptions** and edge cases
* Apply the **@patch** decorator and **context managers** effectively
* Understand **memoization**, **fixtures**, and **integration testing**
* Separate unit tests (isolated) from integration tests (combined components)

---

## 🧩 Project Structure

```
0x03-Unittests_and_integration_tests/
│
├── utils.py
├── client.py
├── fixtures.py
│
├── test_utils.py
└── test_client.py
```

---

## 🧠 Key Components

### 1. **`utils.py`**

Contains helper functions:

* `access_nested_map` – safely access values in nested dicts
* `get_json` – fetch and return JSON data from a given URL
* `memoize` – caching decorator to avoid redundant computations

### 2. **`client.py`**

Implements:

* `GithubOrgClient` – a client for interacting with the GitHub API

  * Fetches organization data
  * Lists repositories
  * Filters by license type

---

## 🧪 Tests Overview

### 🔹 `test_utils.py`

#### Task 0: Parameterize a Unit Test

* Tests `access_nested_map` with various nested paths.
* Uses `@parameterized.expand` and `assertEqual` for concise validation.

#### Task 1: Parameterize a Unit Test (Exception)

* Verifies that invalid paths raise `KeyError` with the correct message.
* Uses `assertRaises` and parameterized input cases.

#### Task 2: Mock HTTP Calls

* Tests `get_json` without making real HTTP requests.
* Mocks `requests.get` and asserts it’s called once with the correct URL.

#### Task 3: Parameterize and Patch

* Tests the `memoize` decorator.
* Verifies that memoized methods call their source method only once.
* Uses `patch` to mock `a_method`.

---

### 🔹 `test_client.py`

#### Task 4: Parameterize and Patch as Decorators

* Tests `GithubOrgClient.org` method using `@patch`.
* Ensures `get_json` is called once with the correct endpoint.

#### Task 5: Mocking a Property

* Tests `_public_repos_url` property.
* Uses context-managed patching to simulate API payloads.

#### Task 6: More Patching

* Tests `public_repos` method.
* Mocks both `get_json` and `_public_repos_url`.
* Verifies repo list and call counts.

#### Task 7: Parameterize

* Tests `has_license` method.
* Uses `@parameterized.expand` to check different license keys and expected boolean outcomes.

---

### 🔹 Integration Tests

#### Task 8: Integration Test (Fixtures)

* Creates `TestIntegrationGithubOrgClient` class using `@parameterized_class`.
* Loads fixture data from `fixtures.py`:

  * `org_payload`, `repos_payload`, `expected_repos`, `apache2_repos`
* Patches `requests.get` globally in `setUpClass` and tears it down after tests.

#### Task 9: Integration Tests (Public Repos)

* Tests the real behavior of `GithubOrgClient.public_repos`.
* Validates output against `expected_repos` and `apache2_repos`.
* Ensures filtering by license works as expected.

---

## 🧾 Example Usage

Run all tests:

```bash
$ python3 -m unittest discover -v
```

Run specific test file:

```bash
$ python3 -m unittest test_utils
$ python3 -m unittest test_client
```

---

## 🧰 Tools & Libraries

* **unittest** – standard Python testing framework
* **parameterized** – simplifies running multiple test cases
* **unittest.mock** – for patching and mocking dependencies
* **requests** – for HTTP interactions (mocked during tests)

---

## 🧱 Best Practices Followed

* All functions, classes, and modules include **docstrings**
* All functions are **type-annotated**
* Each test follows the **AAA (Arrange, Act, Assert)** pattern
* Mocks are used only where necessary (no external API calls)
* Integration tests simulate realistic scenarios with controlled data

---

## 🏁 Summary

This project demonstrates a full testing lifecycle:

| Type                 | Focus                         | Example                          |
| -------------------- | ----------------------------- | -------------------------------- |
| **Unit Test**        | Isolated component logic      | `utils.access_nested_map`        |
| **Mocked Test**      | Replace external dependencies | `get_json` & `requests.get`      |
| **Integration Test** | Combined behavior             | `GithubOrgClient.public_repos()` |

Together, these tests ensure code reliability, performance, and maintainability — essential qualities in any production-grade backend system.

---

### ✍️ Author

**Abubakar Aminu**
*“Test early, test often, and test smart.”*

---

Would you like me to also generate a matching **braglist (dev journal)** for this entire testing project once you’re ready to push?
It’ll summarize all 10 tasks in “Problem → Action → Result” format for your portfolio and LinkedIn.
