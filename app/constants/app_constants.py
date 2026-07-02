# app/constants/app_constants.py

MODEL_NAME = "llama-3.3-70b-versatile"
MODEL_TEMPERATURE = 0.0
MAX_QUESTION_LENGTH = 500

class TraceTags:
    ENV_DEV = "env:dev"
    APP = "langsmith-lab"

class FeedbackKey:
    USER_SCORE = "user_score"

HELPFUL_SCORE = 1.0
UNHELPFUL_SCORE = 0.0