
import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: A number of stars below 1 or above 5 must be refused.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: Invalid types or missing stars must be refused.
@pytest.mark.parametrize(
    "stars, expected_error",
    [
        (
            3.5,
            "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int",
        ),
        (
            "3",
            "json: cannot unmarshal string into Go struct field Rating.stars of type int",
        ),
        (
            None,
            STARS_ERROR,
        ),
    ],
)
def test_invalid_stars_input(api, auth, pizza_id, stars, expected_error):
    new = {"pizza_id": pizza_id}

    if stars is not None:
        new["stars"] = stars

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": expected_error}


# C3: A nonexistent pizza ID must be refused.
def test_nonexistent_pizza_id(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {
        "error": "pizza ID 999999999 not found"
    }


# C4: Missing or invalid authorization must be refused.
@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": "token short"},
    ],
)
def test_invalid_authorization(api, pizza_id, headers):
    new = {"pizza_id": pizza_id, "stars": 3}

    res = api.post("/api/ratings", json=new, headers=headers)

    assert res.status_code == 401
    assert res.json() == {
        "error": "authentication failed"
    }
