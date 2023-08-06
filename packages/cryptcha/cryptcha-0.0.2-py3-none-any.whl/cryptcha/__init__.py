from json import dumps
import requests
import random


class CaptchaClient:
    def __init__(this):
        this.session = requests.Session()
        this.api = {
            "new_token": "https://api.beliefs.repl.co/api/render",
            "validate_token": "https://api.beliefs.repl.co/api/validate",
        }
        this.creator = {"Replit": "/@beliefs", "GitHub": "/ledges"}

    def generate_token(this):
        return dumps(
          this.session.get(this.api["new_token"]).json(),
          indent=2
        )

    def validate(this, token: str):
        return dumps(
            this.session.post(
                this.api["validate_token"], json={"captcha": token}
            ).json(),
            indent=2,
        )
