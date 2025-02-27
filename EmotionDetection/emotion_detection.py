"""
Module for detecting emotions from text using Watson NLP EmotionPredict.
"""

import json
import requests


def emotion_detector(text_to_analyze: str) -> dict:
    """
    Send a POST request to the Watson NLP 'EmotionPredict' endpoint and
    return a dictionary of specific emotions (anger, disgust, fear, joy,
    sadness) along with the dominant emotion.

    :param text_to_analyze: The text to be analyzed for emotions.
    :return: A dictionary with emotion scores and the dominant emotion.
    :raises KeyError: If the expected emotion data is not found in the response.
    """

    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "Content-Type": "application/json",
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 400:
        # Return a dictionary with None values
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }
        
    data = json.loads(response.text)

    try:
        # Extract the emotion dictionary from the API response.
        # The actual response contains an "emotionPredictions" key, which is a list.
        emotions = data["emotionPredictions"][0]["emotion"]
    except (KeyError, IndexError) as e:
        raise KeyError(
            "Expected emotion data not found in API response. "
            "Full response: {}".format(data)
        ) from e

    anger_score = emotions.get("anger", 0.0)
    disgust_score = emotions.get("disgust", 0.0)
    fear_score = emotions.get("fear", 0.0)
    joy_score = emotions.get("joy", 0.0)
    sadness_score = emotions.get("sadness", 0.0)

    # Determine the dominant emotion based on the highest score.
    emotion_dict = {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
    }
    dominant_emotion = max(emotion_dict, key=emotion_dict.get)

    return {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
        "dominant_emotion": dominant_emotion,
    }
