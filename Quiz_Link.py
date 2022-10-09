from KoHisQG.KoHisQGGenerate.KoHisQGGenerate import KoHisQGGenerator
from KoHisQG.KoHisQGVerify.KoHisQGVerify import KoHisQGVerifier
import requests

class KoHisQuizLink:
    def __init__(self) -> None:
        self.quizGenerator = KoHisQGGenerator()
        self.quizVerifier = KoHisQGVerifier()
        self.url = "http://192.168.0.114:3000/quiz"

    def quiz_generate(self):
        generate_data = self.quizGenerator.QGGenerate()
        verified_data = self.quizVerifier.QGVerify(generate_data)

        headers = {}
        response = requests.request("POST", self.url, headers=headers, data=verified_data)