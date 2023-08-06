import json


async def test_get_example(jp_fetch):
    # When
    response = await jp_fetch("jupyterlab_rtc", "get_example")

    # Then
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {
        "data": "This is /datalayer/get_example endpoint!"
    }