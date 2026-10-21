"""Fixtures for the test suite."""
from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from app import app as flask_app

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(name="app")
def configured_app():
    """Return the Flask app configured for testing."""
    flask_app.config.update(TESTING=True)
    yield flask_app


@pytest.fixture(name="client")
def flask_client(app):
    """Return a Flask test client."""
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture()
def sample_image_bytes():
    """Return a valid in-memory PNG image."""
    image = Image.new("RGB", (224, 224), color=(255, 255, 255))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


@pytest.fixture()
def sample_image_path():
    """Return the path to a real test image."""
    return PROJECT_ROOT / "test_images" / "2" / "Sign 2 (97).jpeg"


@pytest.fixture()
def mocked_client(client, monkeypatch):
    """Return a client whose prediction functions are mocked."""
    monkeypatch.setattr("app.preprocess_img", lambda stream: "processed-image")
    monkeypatch.setattr("app.predict_result", lambda image: 7)
    return client
