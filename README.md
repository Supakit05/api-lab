## Part A1 — Input Domain Model

Endpoint: POST /api/ratings

| Block | Input characteristic | Base choice | Other choices |
|---|---|---|---|
| C1 | Number of stars | 1–5 (3) | Below 1 (0), above 5 (6) |
| C2 | Type of stars | Whole number (3) | Decimal (3.5), text ("3"), missing |
| C3 | Pizza ID | Existing pizza | Nonexistent pizza (999999999) |
| C4 | Authorization token | Own valid token | No token, invalid-length token |

### Base Choice

- stars: 3
- stars type: integer
- pizza_id: existing pizza
- Authorization: own valid token
- Expected result: HTTP 201
