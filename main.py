import requests
from datetime import datetime
import os

APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
NUTRITIONIX_EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_POST_ENDPOINT = os.environ.get("SHEETY_POST_ENDPOINT")

GENDER = "male"
WEIGHT = 65
HEIGHT = 175
AGE = 24

exercise_text = input("Tell me which exercises tou did: ")


headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

exercise_data = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

response = requests.post(url=NUTRITIONIX_EXERCISE_ENDPOINT,
                         json=exercise_data,
                         headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

bearer_headers = {
    "Authorization": os.environ.get("SHEETY_BEARER_TOKEN")
}

for exercise in result['exercises']:
    sheet_data = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']

        }
    }
    sheet_response = requests.post(url=SHEETY_POST_ENDPOINT, json=sheet_data, headers=bearer_headers)
    print(sheet_response.text)
