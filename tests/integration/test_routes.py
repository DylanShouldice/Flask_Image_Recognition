"""Integration tests for the Flask routes."""

from io import BytesIO

import pytest


def test_home_page(client):
    """The home page should load."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hand Sign Digit" in response.data


def test_prediction_success(mocked_client, sample_image_bytes):
    """A valid upload should render the mocked prediction."""
    response = mocked_client.post(
        "/prediction",
        data={"file": (sample_image_bytes, "digit.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    assert b"File cannot be processed" not in response.data


@pytest.mark.parametrize(
    ("file_contents", "expected_status"),
    [(None, 400), (b"not an image", 200)],
    ids=("missing-file", "invalid-image"),
)
def test_prediction_invalid_upload(client, file_contents, expected_status):
    """Missing and invalid uploads should show the error message."""
    data = {} if file_contents is None else {"file": (BytesIO(file_contents), "bad.jpg")}
    response = client.post("/prediction", data=data, content_type="multipart/form-data")

    assert response.status_code == expected_status
    assert b"File cannot be processed" in response.data


def test_prediction_get_not_allowed(client):
    """The prediction route only accepts POST."""
    response = client.get("/prediction")
    assert response.status_code == 405
