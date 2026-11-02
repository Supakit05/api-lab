# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: A Calm Quattro Formaggi

- Step 0.12, results of the three runs without a session (optional):
  - Run 1: FAILED
  - Run 2: FAILED
  - Run 3: FAILED

## Step 0.16 — Bug Hunt Checkpoint

### Defect 1: Excluding all tools

- Endpoint: POST /api/pizza
- Input: {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
- Expected: HTTP 400 with a JSON error message
- Actual: HTTP 500
- Description: The API returns an internal server error when all available tools are excluded.
- Test handling: pytest.mark.xfail(reason="Defect 1", strict=True)

### Test Results

- 17 passed
- 1 xfailed
- 0 failed


## Part A3 — Boundary Value Testing

Endpoint: PUT /api/ratings/{id}

| Stars | Expected Status | Result |
|---|---|---|
| 0 | 400 | PASSED |
| 1 | 200 | PASSED |
| 5 | 200 | PASSED |
| 6 | 400 | PASSED |

Boundary values 0 and 6 are rejected, while 1 and 5 are accepted.

Test Results: 4 passed.


## Part A4 — Rating Ownership

### Test Results

| Operation | Actual Status | Result |
|---|---|---|
| GET another user's rating | 404 | PASSED |
| PUT another user's rating | 400 | PASSED |
| DELETE another user's rating | 400 | PASSED |

### Observation

A user cannot read, update, or delete a rating owned by another user.

GET returns HTTP 404 with "not found".

PUT and DELETE return HTTP 400 with a message indicating that the rating ID was not found.

The original rating remains unchanged and accessible to its owner.

All 3 ownership tests passed.


## Part B — Reflection Questions

### 1. Integration Testing vs Unit Testing

These tests are integration tests because they send real HTTP requests to the QuickPizza API and check the responses from the server.

Unlike unit tests, they test the interaction between the client, API, authentication, and stored data rather than testing individual functions in isolation.

### 2. Why create a new user for each test?

Creating a new user for each test keeps the tests independent.

Each user has their own token and ratings, so data created by one test does not affect another test.

This also helps make the test results more reliable.

### 3. Why use requests.Session()?

A Session keeps cookies between HTTP requests.

In this lab, cookies can help requests reach the same backend server during registration and login.

Without a Session, the requests may reach different servers, which can make the test unreliable.

### 4. What defect was found with excludedTools?

When all three available tools were excluded, the API returned HTTP 500 instead of rejecting the request with HTTP 400 and a JSON error message.

Input:
{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}

Actual result: HTTP 500

Expected result: HTTP 400 with a JSON error message

We marked this known defect using pytest.mark.xfail with strict=True.

### 5. Why use Base Choice Testing instead of all combinations?

Base Choice Testing starts with one valid input combination and changes one characteristic at a time.

For POST /api/ratings, the characteristics are stars value, stars type, pizza ID, and authorization token.

Testing every combination would require:

3 × 4 × 2 × 3 = 72 combinations.

Base Choice Testing reduces the number of tests while still covering important input variations.

### 6. What happened when another user accessed a rating?

A second user could not access a rating belonging to the first user.

The API returned:
- GET: HTTP 404
- PUT: HTTP 400
- DELETE: HTTP 400

The original rating remained accessible to its owner and was not modified.



### 7. What happens when using a made-up authentication token?

I tested GET /api/ratings using a made-up token:

Authorization: token 0000000000000000

The API returned HTTP 200 OK and a JSON response containing ratings.

I also tested the same endpoint without an Authorization header.

The API returned HTTP 401 Unauthorized with the error message "authentication failed".

This shows that the API rejects requests without a token but accepted the made-up token in this test.

This unexpected behavior needs further investigation to determine how the API validates authentication tokens.


### 8. API Testing vs UI Testing

API testing checks endpoints, HTTP status codes, JSON responses, authentication, and data operations directly.

UI testing checks how users interact with a website, including buttons, forms, and displayed information.

API testing is useful for checking backend behavior without using a browser, while UI testing checks the user-facing experience.
