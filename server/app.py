#-*- coding: utf-8 -*-

import imp
import json
import logging
import sys
import tornado.gen
import tornado.ioloop
import tornado.log
import tornado.web
from datetime import datetime
from posixpath import join
from traceback import format_exc
from uuid import uuid4

MODEL_DIR = '/code'
MODEL_LIB_DIR = join(MODEL_DIR, 'lib')
sys.path.insert(0, MODEL_DIR)
sys.path.insert(1, MODEL_LIB_DIR)

import main

logging.basicConfig(level=logging.DEBUG)
SERVER_PORT = 9999


class LogFormatter(tornado.log.LogFormatter):

    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt=('%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno'
                 ')d %(levelname)s]%(end_color)s %(message)s'),
            datefmt='%Y-%m-%d %H:%M:%S'
        )


class MainHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, model_id):
        request = self.request
        authorization = request.headers.get('AUTHORIZATION', '')
        try:
            token_type, access_token = authorization.split(' ', 1)
        except Exception as e:
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps({
                "code": 403,
                "data": None,
                "msg": "access_token 已失效或错误"
            }))
            return
        params = {}
        for name in request.query_arguments.keys():
            params[name] = self.get_query_argument(name)
        biosample_id = params.get('biosample_id')
        event = {
            'biosample_id': biosample_id,
            'access_token': access_token,
            'params': params
        }
        context = {}
        event = json.dumps(event)
        try:
            result = main.handler(event, context)
        except Exception:
            exc = format_exc()
            result = {
                "task_msg": "任务执行失败，错误：{}".format(exc),
                "estimated_runtime": None,
                "completed": datetime.now().strftime('%Y-%m-%dT%H:%M:%M+0800'),
                "progress": "FAILURE",
                "result": None,
                "task_id": uuid4().hex
            }
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps({
                'code': 0,
                'msg': 'success',
                'data': result
            }))
            return
        try:
            result = json.loads(result)
        except ValueError:
            return self.error_handler(
                500, msg='Model response expects a json dict string.'
                    .format(result))
        if not isinstance(result, dict):
            return self.error_handler(
                500, msg='Model response expects a json dict string.'
                    .format(result))
        for field in ('model_code', 'model_msg', 'model_data'):
            if field not in result:
                return self.error_handler(41402, '函数计算模型返回值 json 格式错误')
        model_code = result['model_code']
        if model_code != 0 and (model_code < 47000 or model_code > 47999):
            return self.error_handler(
                41403, 'model_code 取值范围：0 或 [47000, 47999], 当前返回：{}'
                    .format(model_code))
        self.set_header('Content-Type', 'application/json')
        result = {
            "task_msg": "任务执行成功",
            "estimated_runtime": None,
            "completed": datetime.now().strftime('%Y-%m-%dT%H:%M:%M+0800'),
            "progress": "SUCCESS",
            "result": result,
            "task_id": uuid4().hex
        }
        self.write(json.dumps({
            'code': 0,
            'msg': 'success',
            'data': result
        }))

    def error_handler(self, code, msg, data=None):
        self.set_header('Content-Type', 'application/json')
        self.write({
            'code': code,
            'data': data,
            'msg': msg
        })


def make_app():
    [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
    return tornado.httpserver.HTTPServer(tornado.web.Application([
        (r"\/model\/([0-9a-zA-Z]+)", MainHandler),
    ], debug=True))


if __name__ == "__main__":
    app = make_app()
    app.listen(SERVER_PORT)
    print('Starting server at http://0.0.0.0:{}/'.format(SERVER_PORT))
    print('Quit the server with CONTROL-C.')
    tornado.ioloop.IOLoop.current().start()
