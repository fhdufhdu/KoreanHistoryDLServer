from flask import Flask, request
from flask_restx import Api
from flask_cors import CORS
from QnA_Link import KoHisQnALink
from Quiz_Link import KoHisQuizLink
import time
import schedule
from threading import Thread

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['JSON_AS_ASCII'] = False
koHisQnA = KoHisQnALink()
koHisQuiz = KoHisQuizLink()

def quiz():
    schedule.every().monday.at("00:00").do(koHisQuiz.quiz_generate)

    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/qna', methods=["GET", "POST"])
def qna():
    # if request.method == "GET":
    #     data = urllib.parse.urlencode(request.args, doseq=True)
    #     decoded_data = urllib.parse.parse_qs(data, encoding='utf-8')

    #     key_list = []
    #     for key in decoded_data:
    #         key_list.append(key)

    #     resp = {}
    #     for key in key_list:
    #         resp[key] = decoded_data[key]

    #     return resp

    if request.method == "POST":
        data = request.get_json()
        
        key_list = []
        for key in data:
            key_list.append(key)

        question = data[key_list[0]]
        resp = koHisQnA.get_qna_result(question)

        return resp

if __name__ == "__main__":
    works = []
    works.append(Thread(target=quiz))

    for work in works:
        work.start()
    
    app.run(host=("202.31.202.147"), debug=True)

## GET, PUT, DELETE -> request.args.get('key)
## POST -> request.get_json()
## State Code -> 200 : sucees
##               400 : not variable parapeter or false request
##               401 : not aloow access
##               403 : ban access
##               404 : Not found resource
##               500 : internal serverl error