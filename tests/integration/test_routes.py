from io import BytesIO


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


def test_prediction_missing_file(client):
    """Posting without a file should show the error message."""
    response = client.post(
        "/prediction",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed" in response.data


def test_prediction_invalid_image(client):
    """Posting a non-image file should show the error message."""
    response = client.post(
        "/prediction",
        data={"file": (BytesIO(b"not an image"), "bad.jpg")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed" in response.data


def test_prediction_get_not_allowed(client):
    """The prediction route only accepts POST."""
    response = client.get("/prediction")
    assert response.status_code == 405
