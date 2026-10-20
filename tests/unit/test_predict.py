import numpy as np
import pytest

from model import predict_result


class FakeModel:
    """Small stand-in for the Keras model."""

    def predict(self, _image):
        """Return fixed probabilities where class 2 is highest."""
        return np.array([[0.1, 0.2, 0.7]])


def test_predict_result_returns_argmax(monkeypatch):
    """predict_result should return the index of the highest probability."""
    monkeypatch.setattr("model.model", FakeModel())
    result = predict_result(np.zeros((1, 224, 224, 3)))
    assert result == 2


def test_predict_result_is_integer(sample_image_path):
    """A real prediction should be an integer digit."""
    from model import preprocess_img

    image = preprocess_img(sample_image_path)
    prediction = predict_result(image)

    assert isinstance(prediction, (int, np.integer))
    assert 0 <= prediction <= 9


@pytest.mark.slow
def test_prediction_is_consistent(sample_image_path):
    """The same image should produce the same prediction."""
    from model import preprocess_img

    image = preprocess_img(sample_image_path)
    predictions = {predict_result(image) for _ in range(3)}
    assert len(predictions) == 1
