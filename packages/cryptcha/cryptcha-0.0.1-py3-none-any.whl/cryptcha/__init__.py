import requests
import random


class CaptchaClient:
    def __init__(this):
        this.session = requests.Session()
        this.api = {
            "new_token": "https://api.beliefs.repl.co/api/render",
            "validate_token": "https://api.beliefs.repl.co/api/validate",
        }
        this.creator = {
          "Replit": "/@beliefs", 
          "GitHub": "/ledges"
        }

    def generate_token(this):
      return this.session.get(this.api["new_token"]).json()

    def validate(this, token: str):
      return this.session.post(this.api["validate_token"], json={"captcha": token}).json()
