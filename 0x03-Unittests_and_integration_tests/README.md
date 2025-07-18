### Unit Tests for access_nested_map Function
Overview
### This project implements parameterized unit tests for the access_nested_map function from the utils module. The tests validate that the function correctly accesses values in nested dictionaries using specified paths.

### Key Features
Parameterized testing using @parameterized.expand

Three test cases covering different access scenarios

Concise test implementation (≤2 lines per test case)

Test Cases
Top-level access
nested_map={"a": 1}, path=("a",) → Expected: 1

Nested dictionary access
nested_map={"a": {"b": 2}}, path=("a",) → Expected: {"b": 2}

Deeply nested value access
nested_map={"a": {"b": 2}}, path=("a", "b") → Expected: 2
