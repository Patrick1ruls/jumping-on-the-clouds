# Files of Interest
* Tests located in ```test_hash_server.py```
* Test cases located in ```test_cases.md```
* Bug report located in ```bug_reportmd```

# How to Run Tests
* Make sure you have pytest and pytest-xdist installed: 
    ```
    pip install pytest
    pip install pytest-xdist
    ```
* This will enable you to run all tests in parallel
* Run tests in test directory with:
    ```
    pytest -n 23
    ```

# Example Output
```
============================================================ short test summary info =============================================================FAILED test_hash_server.py::test_hash_collison[payload_10-payload_20] - AssertionError: Hash collision detected
FAILED test_hash_server.py::test_hash_collison[payload_12-payload_22] - AssertionError: Hash collision detected
FAILED test_hash_server.py::test_duplicate_hashes - AssertionError: Duplicate hash stored in db
FAILED test_hash_server.py::test_hash_collison[payload_13-payload_23] - AssertionError: Hash collision detected
FAILED test_hash_server.py::test_hash_collison[payload_11-payload_21] - AssertionError: Hash collision detected
========================================================= 5 failed, 18 passed in 13.22s ==========================================================
```