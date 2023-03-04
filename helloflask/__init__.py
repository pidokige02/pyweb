from flask import Flask, g, request, Response, make_response
from datetime import datetime, date

app = Flask(__name__)
app.debug = True     # use only debug!!


@app.route('/reqenv')
def reqenv(): # %(REQUEST_METHOD) 안에 request.environ["REQUEST_METHOD"] 이 들어간다.
    return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
            'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
            'PATH_INFO: %(PATH_INFO) s <br>'
            'QUERY_STRING: %(QUERY_STRING) s <br>'
            'SERVER_NAME: %(SERVER_NAME) s <br>'
            'SERVER_PORT: %(SERVER_PORT) s <br>'
            'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
            'wsgi.version: %(wsgi.version) s <br>'
            'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
            'wsgi.input: %(wsgi.input) s <br>'
            'wsgi.errors: %(wsgi.errors) s <br>'
            'wsgi.multithread: %(wsgi.multithread) s <br>'
            'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
            'wsgi.run_once: %(wsgi.run_once) s') % request.environ

# # request 처리 용 함수
# def ymd(fmt): #함수 trans 를 정의하고 return 한다 return 한 함수는 아래 ymt call 시 대치된다
#     def trans(date_str): # date_str 은 date parameter(ex : 2019-02-26) 를 준다 ()
#         return datetime.strptime(date_str, fmt)
#     return trans

# # http://127.0.0.1:5000/dt?date=2019-05-2 와 같이 부르거나 param 이 없으면 오늘 날짜가 사용된다
# @app.route('/dt')
# def dt():
#     datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
#     return "우리나라 시간 형식: " + str(datestr)

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
