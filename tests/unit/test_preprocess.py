import numpy as np
import pytest

from model import preprocess_img


def test_preprocess_img_shape(sample_image_path):
    """The processed image should have the shape expected by the model."""
    result = preprocess_img(sample_image_path)
    assert result.shape == (1, 224, 224, 3)


def test_preprocess_img_is_normalized(sample_image_path):
    """Pixel values should be normalized between 0 and 1."""
    result = preprocess_img(sample_image_path)
    assert np.min(result) >= 0.0
    assert np.max(result) <= 1.0


def test_preprocess_img_missing_file():
    """A missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        preprocess_img("test_images/does-not-exist.jpg")
