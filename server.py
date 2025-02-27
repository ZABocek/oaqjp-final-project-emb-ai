"""
A Flask web application for emotion detection.
"""

from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/emotionDetector", methods=["GET", "POST"])
def detect_emotion():
    """
    Flask endpoint to detect emotion from user input text.
    If the request is POST, the text is read from form data with key 'text'.
    If the request is GET, the text is read from query parameters with key 'textToAnalyze'.
    """
    if request.method == "POST":
        text_to_analyze = request.form.get("text")
    else:
        text_to_analyze = request.args.get("textToAnalyze")

    if not text_to_analyze:
        return "No text provided"

    result = emotion_detector(text_to_analyze)
    response_str = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return response_str


@app.route("/")
def index():
    """
    Render the main page with the form.
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
