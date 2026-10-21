"""Model for image recognition. Houses the functions for
pre-processing the image and predicting the result"""
# Importing required libs
from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image

# Loading model
model = load_model("digit_model.h5")


# Preparing and pre-processing the image
def preprocess_img(img_path):
    """Pre-processes the image to be compatible with the model."""
    op_img = Image.open(img_path)
    img_resize = op_img.resize((224, 224))
    img2arr = img_to_array(img_resize) / 255.0
    img_reshape = img2arr.reshape(1, 224, 224, 3)
    return img_reshape


# Predicting function
def predict_result(predict):
    """Predicts the result of the pre-processed image."""
    pred = model.predict(predict)
    return np.argmax(pred[0], axis=-1)
