from flask import Flask, g, Response, make_response

app = Flask(__name__)
app.debug = True     # use only debug!!

@app.before_request  # request 를 처리하기 전에 실행하여 주세요
def before_request():
    print("before_request!!!")
    g.str = "한글"

# response_class
@app.route("/res1")
def res1():  #test :111 은 header 에 실린다
    custom_res = Response("Custom Response", 200, {'test': 'ttt'})
    return make_response(custom_res)

@app.route("/res2")
# str : Simple String (HTML, JSON)
def res2():
    return make_response("custom response")

@app.route("/")
def helloworld():
    return "Hello World!" + getattr(g, 'str', '111')  # '111' 은 default 값임
