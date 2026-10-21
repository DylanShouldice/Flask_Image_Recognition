""" App.py houses the endpoints for the flask app. / = root, /prediction = prediction route. """
# Importing required libs
from flask import Flask, render_template, request
from model import preprocess_img, predict_result

# Instantiating flask app
app = Flask(__name__)


# Home route
@app.route("/")
def main():
    """Returns the home page of the flask app."""
    return render_template("index.html")


# Prediction route
@app.route("/prediction", methods=["POST"])
def predict_image_file():
    """Returns the prediction result of the uploaded image file."""
    try:
        if request.method == "POST":
            img = preprocess_img(request.files["file"].stream)
            pred = predict_result(img)
            return render_template("result.html", predictions=str(pred))

    except (FileNotFoundError, ValueError):
        error = "File cannot be processed."
        return render_template("result.html", err=error)
    return render_template("result.html", err="File cannot be processed.")


# Driver code
if __name__ == "__main__":
    app.run(port=9000, debug=True)
