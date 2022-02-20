#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : wechat_push
# @Date : 2022-02-22
# @Project: PKUElective2022Spring-main
# @AUTHOR : Totoro
import http.client
import socket
import urllib.parse
import json
from timeit import default_timer as timer
from socket import gaierror as GetAddressError


class Notify(object):

    @property
    def disable_push(self):
        return self._disable_push

    @property
    def get_token(self):
        return self._token

    @property
    def get_verbosity(self):
        return self._verbosity

    @property
    def get_interval_lock(self):
        return self._interval_lock

    def get_time_stamp(self):
        return self._time_stamp

    def get_elapsed_time(self):
        return timer() - self.get_time_stamp()

    def output_ready(self):
        return self.get_elapsed_time() >= self.get_interval_lock

    def __init__(self, _token, _interval_lock, _disable_push=0, _verbosity=2):
        self._disable_push = _disable_push
        self._token = _token
        self._time_stamp = timer()
        self._interval_lock = _interval_lock
        self._verbosity = _verbosity

    def send_wechat_push(self, token=None, msg: str = '', prefix: str = '', server: str = "push.jwks123.cn", port: int = 443):
        try:
            if self.disable_push == 1:
                return
            if token is None:
                token = self.get_token
            if not token or not msg or not self.output_ready():
                return

            if port == 443:
                conn = http.client.HTTPSConnection(host=server, port=port)
            else:
                conn = http.client.HTTPConnection(host=server, port=port)
            rqbody = json.dumps(dict(token=token, msg=prefix + msg))
            conn.request(method="POST", url="/to/", body=rqbody)
            resp = conn.getresponse()
            rs = json.loads(resp.read().decode("utf8"))
            assert int(rs["code"] / 100) == 2, rs

        except AssertionError as e:
            print("网络连接错误\n")

        except ValueError as err_val:
            print(self.get_token)
            print("公众号提醒设置有误，请检查您传入的token值\n")

        except GetAddressError as err_connect:
            print("网络连接错误\n")

        except BaseException as e:
            print("公众号提醒设置有误,推送发送失败\n")

        finally:
            self._time_stamp = timer()


def test_notify(_token_: str):
    notify = Notify(_token=_token_, _interval_lock=0, _disable_push=0, _verbosity=2)
    notify.send_wechat_push(msg='This is a test.', prefix='[测试]')


test_notify('')  # 在单引号内填入您的token
