from flask import Flask, g, request, Response, make_response
from flask import session, render_template, Markup, url_for
from datetime import date, datetime, timedelta
import os
from helloflask.init_db import init_database, db_session

import os

app = Flask(__name__)
import helloflask.views   #view 를 등록하여야 views 에 있는 router 가 실행된다.
import helloflask.tests
import helloflask.filters

app.debug = True     # use only debug!!

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime) # modified 된 시간을 key 값 q에 집어넣는다.
    return url_for(endpoint, **values)
# 이함수는 static folder 아래 file 로의 URL을 변경시킨다. original+?qxxxx


@app.context_processor  # # context 가 만들어질 경우 어떻게 할 것인가.
def override_url_for():
    return dict(url_for=dated_url_for)  ##url_for을 불렀을 경우는 dated_url_for 로 가라. (flask의 확장기능임)

app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days  cf. minutes=30
)

@app.before_first_request
def beforeFirstRequest():
    print(">> before_first_request!!")
    init_database()   # initialize database


@app.after_request
def afterReq(response):
    print(">> after_request!!")
    return response


@app.teardown_request  # request가 소멸될때
def teardown_request(exception):
    print(">>> teardown request!!", exception)


@app.teardown_appcontext  #response 까지 모두 끝났을 때.
def teardown_context(exception):
    print(">>> teardown context!!", exception)
    db_session.remove()   # remove used db-session
