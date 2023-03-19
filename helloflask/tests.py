from flask import Flask, g, request, Response, make_response
from flask import session, render_template, Markup, url_for
from datetime import datetime, date
from collections import namedtuple
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from helloflask import app
from helloflask.classes import Nav, FormInput

from helloflask.init_db import db_session
from helloflask.models import User, Song, Album, Artist, SongArtist

@app.route('/sqltest')
def sqltest():
    ret = 'OK'
    try:
        # sample codes 1 for add and field update
        # u = User('11abc@efg.com', 'hong')
        # db_session.add(u)
        # u = User('12abc@efg.com', 'hong')
        # db_session.add(u)
        # u = User.query.filter(User.id == 2).first()
        # print("user.id", u.id)
        # u.email = 'pidokige.naver.com'
        # db_session.add(u)

        # db_session.commit()  # session made by flask
        # ret = User.query.all()  # query all data.

        # sample codes 2 for update

        # sample codes 3 for select
        # 아래보다는 위와 같이 class를 만들어 쓰는 것이 좋은 codes임
        s = db_session()
        result = s.execute(text('select id, email, nickname from User where id > :id'), {'id': 5})
        print(">>", result.keys())
        Record = namedtuple('User', result.keys()) # list type 을 map type 을 변경한다.
        rrr = result.fetchall()  # tuple 의 list 형태로 반환됨

        for r in rrr:
            print(r)  # display as tuple type

        for r in rrr:
            print(*r) # display as "tuple 이 제거된 형태임"

        print(">>", type(result), result.keys(), rrr)
        records = [Record(*r) for r in rrr] # *r 은 rrr 에 있는 것을 모두 다 주세요라는 의미임
        for r in records:
            print(r, r.nickname, type(r))

        s.close()
        ret = records

    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        print("SqlError>>", sqlerr)

    except:
        print("Error!!")

    finally:
        db_session.close()

    # return "RET=" + str(ret)
    return render_template('main.html', userlist=ret)

@app.route('/sql3')
def sql3():
    # albums = Album.query.order_by(Album.albumid.desc()).limit(5)
    # albums = Album.query.filter(Album.albumid == '0000001').all()

    albums = Album.query.options(joinedload(
        Album.songs)).filter_by(albumid='0000002').all()

    return render_template('main.html', albums=albums)

# pre-load (sametime)
@app.route('/sql2')
def sql2():
# 아래 two case 가 모두 같은 기능으로 동작함 (subqueryload vs joinedload) w/ backref
    # ret = db_session.query(Song).options(subqueryload(Song.album))\
    #       .filter(Song.likecnt < 10000)

    ret = Song.query.options(joinedload(Song.album))\
              .filter(Song.likecnt < 10000)

    return render_template('main.html', ret=ret)

# select by each record
@app.route('/sql')
def sql():
    # song 만 select 했는데 album 의 title 조회가 가능함 (in main.html)(ORM 의 power)
    # ret = Song.query.filter(Song.likecnt < 10000) # backref enable 생태에서 test 함
    # ret = Song.query.join(Album, Song.albumid == Album.albumid).filter(Song.likecnt < 10000)
    # 위 2 codes 는 같은 기능을 하는 것임

    ret = Song.query.options(joinedload(Song.album)).filter(Song.likecnt < 10000).options(joinedload(Song.songartists, SongArtist.artist))

    # ret = Song.query.options(joinedload(Song.album)).filter(Song.likecnt < 10000).options(joinedload(Song.songartists)).options(
    #     subqueryload(Song.songartists, SongArtist.artist)).order_by('atype')
    return render_template('main.html', ret=ret)

@app.route('/addref')
def addref():
    aid = 'TTT-a1'
    a1 = Album.query.filter(Album.albumid==aid)
    print("a1=----------->>", a1, a1.count())
    if a1.count() == 0:
        a1 = Album(albumid=aid, title='TTT-album')
    else:
        a1 = a1.one()

    song1 = Song(songno='TTT3', title='TTT3 Title')
    song1.album = a1

    # 1 : n
    # song1.albums = [ a1, a2 ] #song 에 album 이 여러개 일 경우 assign 하는 방법

    # album 이 db 에 없으면 song만 넣어도 db에 song 과 같이 들어간다.
    db_session.add(song1)
    db_session.commit()

    print("song1=", song1)
    return "OK"

# http://127.0.0.1:5000/calendar
@app.route('/calendar')
def calendar():
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
