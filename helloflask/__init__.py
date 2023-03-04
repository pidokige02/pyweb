from flask import Flask, g

app = Flask(__name__)
app.debug = True     # use only debug!!

@app.before_request  # request 를 처리하기 전에 실행하여 주세요
def before_request():
    print("before_request!!!")
    g.str = "한글"

@app.route("/")
def helloworld():
    return "Hello World!" + getattr(g, 'str', '111')  # '111' 은 default 값임
