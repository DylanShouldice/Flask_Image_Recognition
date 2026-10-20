import re
from io import BytesIO
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]

pytestmark = [pytest.mark.slow, pytest.mark.acceptance]

DIGIT_IN_RESULT_PAGE = re.compile(
    rb'class="display-4 text-dark font-weight-bold"\s*>\s*([0-9])\s*<'
)

# Each tuple is (image path relative to the project root, expected digit).
REAL_IMAGE_CASES = [
    ("test_images/0/Sign 0 (116).jpeg", 0),
    ("test_images/2/Sign 2 (97).jpeg", 2),
    ("test_images/4/Sign 4 (92).jpeg", 4),
    ("test_images/5/Sign 5 (86).jpeg", 5),
    ("test_images/7/Sign 7 (54).jpeg", 7),
    ("test_images/9/Sign 9 (1).jpeg", 9),
]


def _upload_image(client, image_path):
    """Upload an image file through the prediction endpoint."""
    with image_path.open("rb") as image_file:
        return client.post(
            "/prediction",
            data={"file": (image_file, image_path.name)},
            content_type="multipart/form-data",
        )


def _predicted_digit(response):
    """Extract the predicted digit from the rendered result page."""
    match = DIGIT_IN_RESULT_PAGE.search(response.data)
    assert match is not None, "The result page did not contain a predicted digit"
    return int(match.group(1))


def test_home_page_loads(client):
    """The home page should render successfully."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Hand Sign Digit" in response.data


@pytest.mark.parametrize(("relative_path", "expected_digit"), REAL_IMAGE_CASES)
def test_real_image_prediction(client, relative_path, expected_digit):
    """A real image should be classified as the correct digit end-to-end."""
    image_path = PROJECT_ROOT / relative_path
    assert image_path.is_file(), f"Missing test image: {image_path}"

    response = _upload_image(client, image_path)

    assert response.status_code == 200
    assert b"File cannot be processed" not in response.data
    assert _predicted_digit(response) == expected_digit


def test_sequential_real_image_uploads(client):
    """Multiple uploads should each return their own correct prediction."""
    first_path = PROJECT_ROOT / "test_images/2/Sign 2 (97).jpeg"
    second_path = PROJECT_ROOT / "test_images/5/Sign 5 (86).jpeg"

    first_response = _upload_image(client, first_path)
    second_response = _upload_image(client, second_path)

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert _predicted_digit(first_response) == 2
    assert _predicted_digit(second_response) == 5


def test_missing_file_returns_error_page(client):
    """Submitting without a file should render the error page."""
    response = client.post(
        "/prediction",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed" in response.data


def test_invalid_image_returns_error_page(client):
    """Submitting a non-image file should render the error page."""
    response = client.post(
        "/prediction",
        data={"file": (BytesIO(b"this is not an image"), "not-an-image.jpg")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed" in response.data


def test_edge_case_non_standard_image_extensions(client):
    """
    Test uploading images with non-standard file extensions.
    - Scenario: Upload a file with an uncommon extension, e.g., .webp.
    - Expected Behavior: System processes the file as a valid image.
    """
    relative_path = "test_images/0/Sign 0 (187).webp"
    image_path = PROJECT_ROOT / relative_path
    assert image_path.is_file(), f"Missing test image: {image_path}"

    response = _upload_image(client, image_path)

    assert response.status_code == 200
