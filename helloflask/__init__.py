from flask import Flask, g, request, Response, make_response
from flask import session, render_template, Markup, url_for
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from helloflask.classes import FormInput

import os

app = Flask(__name__)
# import helloflask.views
# import helloflask.tests
import helloflask.filters

app.debug = True     # use only debug!!

app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days  cf. minutes=30
)

# http://127.0.0.1:5000/
@app.route('/')
def idx():
    rds = []
    for i in [1,2,3]:
        id = 'r' + str(i)
        name = 'radiotest'
        value = i
        checked = ''
        if i == 2:
            checked = 'checked'
        text = 'RadioTest' + str(i)
        rds.append( FormInput(id, name, value, checked, text) )
# remard for basic datatime test
    # # today = date.today()
    # # today = datetime.now()
    # today = datetime.strptime('2019-02-14 09:22', '%Y-%m-%d %H:%M')
        today = '2023-03-11 09:22'
    # return render_template('app.html', ttt='TestTTT999', radioList=rds, today=today)
        d = datetime.strptime("2023-03-01", "%Y-%m-%d")
# remark for keeping one month calander
        # sdt = d.weekday() * -1  # 목요일이면 월화수가 빠져버린다
        # nextMonth = d + relativedelta(months=1)
        # mm = d.month
        # edt = (nextMonth - timedelta(1)).day + 1  # 마지말 요일을 계산한
        # return render_template('app.html', sdt=sdt, edt=edt, mm=mm, ttt='TestTTT999', radioList=rds, today=today)

    # year = 2023
    # accessing paramter like /?year=2023
    year = request.args.get('year', date.today().year, int)
    return render_template('app.html', year=year, ttt='TestTTT999', radioList=rds, today=today)

# http://127.0.0.1:5000/top100
@app.route('/top100')
def top100():
    return render_template('application.html', title='MAIN!')

# http://127.0.0.1:5000/main
@app.route('/main')
def main():
    return render_template('main.html', title='MAIN!')

@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다!"

# http://127.0.0.1:5000/wc?key=token&val=abc
# inspection/application/cookie 에 setting 된것을 볼 수 있다.
@app.route('/wc') #write cookies
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response("SET COOKIE")
    res.set_cookie(key, val)
    session["Token"] = '123X' # toekn 을 cookie 와 같이 seting 함
    return make_response(res)


# http://127.0.0.1:5000/rc?key=token
@app.route('/rc') #read cookies
def rc():
    key = request.args.get('key') #token
    val = request.cookies.get(key)
    return "cookie[" + key +"]=" + val + "," + session.get('Token')


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

# request 처리 용 함수
def ymd(fmt): #함수 trans 를 정의하고 return 한다 return 한 함수는 아래 ymt call 시 대치된다
    def trans(date_str): # date_str 은 date parameter(ex : 2019-02-26) 를 준다 ()
        return datetime.strptime(date_str, fmt)
    return trans

# http://127.0.0.1:5000/dt?date=2019-05-2 와 같이 부르거나 param 이 없으면 오늘 날짜가 사용된다
@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)

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

# @app.route("/")
# def helloworld():
#     return "Hello World!" + getattr(g, 'str', '111')  # '111' 은 default 값임
