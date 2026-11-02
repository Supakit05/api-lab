
import pytest


@pytest.mark.parametrize("tool", ["Knife", "Scissors"])
def test_exclude_one_tool(api, auth, tool):
    res = api.post(
        "/api/pizza",
        json={"excludedTools": [tool]},
        headers=auth,
    )

    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] != tool


@pytest.mark.parametrize(
    "excluded",
    [
        [],
        ["Knife"],
        ["Knife", "Scissors"],
        pytest.param(
            ["Knife", "Pizza cutter", "Scissors"],
            marks=pytest.mark.xfail(
                reason="Defect 1: excluding all tools returns HTTP 500 instead of HTTP 400",
                strict=True,
            ),
        ),
    ],
)
def test_excluded_tools_by_count(api, auth, excluded):
    res = api.post(
        "/api/pizza",
        json={"excludedTools": excluded},
        headers=auth,
    )

    assert res.status_code == 200
    pizza = res.json()

    for tool in excluded:
        assert pizza["pizza"]["tool"] != tool
