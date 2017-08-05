# coding=utf8
from flask import Flask
from db import RedisClient

app = Flask(__name__)
rclient = RedisClient()


@app.route('/')
def index():
    return "Hello World"


@app.route('/get')
def get_proxy():
    try:
        proxy = rclient.rand_proxy()
        return proxy
    except:
        pass
    return ''


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12321)
