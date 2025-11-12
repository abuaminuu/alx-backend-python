---

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
