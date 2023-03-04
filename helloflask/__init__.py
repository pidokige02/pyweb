from flask import Flask, g, request, Response, make_response

app = Flask(__name__)
app.debug = True     # use only debug!!

# http://127.0.0.1:5000/rp?q=123 을 실행하면 q=123 이 출력됨
# @app.route('/rp')
# def rp():
#     q = request.args.get('q')
#     return "q=%s" % str(q)

# http://127.0.0.1:5000/rp?q=한글&q=eng 을 실행하면 q=['한글', 'eng'] 이 출력됨
@app.route('/rp')
def rp():
    q = request.args.getlist('q')
    return "q=%s" % str(q)

# @app.before_request  # request 를 처리하기 전에 실행하여 주세요
# def before_request():
#     print("before_request!!!")
#     g.str = "한글"

# response_class
@app.route("/res1")
def res1():  #test :111 은 header 에 실린다
    custom_res = Response("Custom Response", 200, {'test': 'ttt'})
    return make_response(custom_res)

@app.route("/res2")
# str : Simple String (HTML, JSON)
def res2():
    return make_response("custom response")

# Response Objects (Cont'd) : WSGI
# WSGI(WebServer Gateway Interface)
@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):  # inner function 힘
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        # environ['REQUEST_METHOD'] 값이 %s로 들어간다
        headers = [ ('Content-Type', 'text/plain'),
					('Content-Length', str(len(body))) ]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)

@app.route("/")
def helloworld():
    return "Hello World!" + getattr(g, 'str', '111')  # '111' 은 default 값임
