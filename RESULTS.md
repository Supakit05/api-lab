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
